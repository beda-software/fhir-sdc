from typing import Any

import simplejson as json
from aiohttp import ClientSession, web
from fhirpy import AsyncFHIRClient
from fhirpy.base.exceptions import OperationOutcome
from funcy.seqs import flatten

from .mappers import load_mappers
from .utils import (
    build_fhirpath_env,
    check_mappers_bundles_full_url_duplicates,
    resolve_fpml_template,
)


async def get_external_service_bundle(session, service, template, context):
    if not service:
        raise OperationOutcome("No service is configured to render this mapper")

    async with session.post(
        service,
        json={
            "template": template,
            "context": context,
        },
    ) as result:
        if 200 <= result.status <= 299:
            return await result.json()
        else:
            raise web.HTTPBadRequest(body=await result.text())


def build_result_bundle(mappers_bundles: list[dict]) -> dict:
    try:
        # NOTE: `bundle.get("entry", None) or []` is used to catch cases, when
        # bundle is like `{'type': 'transaction', 'entry': None, 'resourceType': 'Bundle'}`
        # This can happen for example when adding the following flag top Mapping
        # params:
        #   omit-drop-blanks: true
        flattened_mappers_bundles = list(
            flatten(bundle.get("entry", None) or [] for bundle in mappers_bundles)
        )
    except:
        flattened_mappers_bundles = []

    check_mappers_bundles_full_url_duplicates(flattened_mappers_bundles)

    not_transaction = any(bundle.get("type") != "transaction" for bundle in mappers_bundles)

    return {
        "resourceType": "Bundle",
        "type": "batch" if not_transaction else "transaction",
        "entry": flattened_mappers_bundles,
    }


async def build_extract_bundle(
    client: AsyncFHIRClient,
    questionnaire: dict,
    questionnaire_response: dict,
    variables: dict[str, Any],
    extract_services: dict,
) -> dict | None:
    """Render the Questionnaire's mappers into one bundle, or None when they render nothing."""
    mappers = await load_mappers(client, questionnaire)
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    async with ClientSession() as session:
        mappers_bundles = []

        for mapper in mappers:
            if "resourceType" in mapper and "body" in mapper:
                # It is custome mapper resource
                mapper_type = mapper.get("type", "JUTE")
                if mapper_type == "FHIRPath" and extract_services["FHIRPath"] == "fpml":
                    result = resolve_fpml_template(
                        mapper["body"],
                        env,
                    )
                    result_no_decimal = json.loads(json.dumps(result))
                    mappers_bundles.append(result_no_decimal)
                else:
                    # Use 3rd party service FHIRPathMapping or JUTE
                    mappers_bundles.append(
                        await get_external_service_bundle(
                            session, extract_services[mapper_type], mapper["body"], env
                        )
                    )
            else:
                # legacy extraction
                mappers_bundles.append(
                    await get_external_service_bundle(
                        session, extract_services["JUTE"], mapper, env
                    )
                )

        # A mapper that renders nothing answers with null, which is not a bundle.
        mappers_bundles = [bundle for bundle in mappers_bundles if bundle]
        return build_result_bundle(mappers_bundles) if mappers_bundles else None
