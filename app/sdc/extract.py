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


async def execute_mappers_bundles(client, mappers_bundles):
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

    result_bundle = {
        "resourceType": "Bundle",
        "type": "batch" if not_transaction else "transaction",
        "entry": flattened_mappers_bundles,
    }

    return await client.execute("/", data=result_bundle)


async def extract(
    client: AsyncFHIRClient,
    questionnaire: dict,
    questionnaire_response: dict,
    variables: dict[str, Any],
    extract_services: dict,
) -> list:
    """Render the Questionnaire's mappers and submit the bundles they produce."""
    mappers = await load_mappers(client, questionnaire)
    env = build_fhirpath_env(questionnaire, questionnaire_response, variables)
    async with ClientSession() as session:
        resp = []
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

        # A mapper that renders nothing answers with null, which is not a bundle to submit.
        mappers_bundles = [bundle for bundle in mappers_bundles if bundle]
        if len(mappers_bundles) > 0:
            resp.append(await execute_mappers_bundles(client, mappers_bundles))

        return resp
