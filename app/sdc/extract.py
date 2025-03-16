from aiohttp import ClientSession, web
from funcy.seqs import flatten

from .utils import check_mappers_bundles_full_url_duplicates, resolve_fpml_template


async def get_external_service_bundle(session, service, template, context):
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
    flattened_mappers_bundles = list(flatten(bundle["entry"] for bundle in mappers_bundles))

    check_mappers_bundles_full_url_duplicates(flattened_mappers_bundles)

    not_transaction = any(bundle.get("type") != "transaction" for bundle in mappers_bundles)

    result_bundle = {
        "resourceType": "Bundle",
        "type": "batch" if not_transaction else "transaction",
        "entry": flattened_mappers_bundles,
    }

    return await client.execute("/", data=result_bundle)


async def extract(client, mappings, context, extract_services):
    """
    mappings could be a list of Aidbox Mapping resources
    or plain jute templates
    """
    async with ClientSession() as session:
        resp = []
        mappers_bundles = []

        for mapper in mappings:
            if "resourceType" in mapper and "body" in mapper:
                # It is custome mapper resource
                mapper_type = mapper.get("type", "JUTE")
                if mapper_type == "JUTE" and extract_services["JUTE"] == "aidbox":
                    mapper_bundle = await mapper.execute("$debug", data=context)
                    if "entry" not in mapper_bundle:
                        continue

                    mappers_bundles.append(mapper_bundle)

                elif mapper_type == "FHIRPath" and extract_services["FHIRPath"] == "fpml":
                    mappers_bundles.append(
                        resolve_fpml_template(
                            mapper["body"],
                            context,
                        )
                    )
                else:
                    # Use 3rd party service FHIRPathMapping or JUTE
                    mappers_bundles.append(
                        await get_external_service_bundle(
                            session, extract_services[mapper_type], mapper["body"], context
                        )
                    )
            else:
                # legacy extraction
                mappers_bundles.append(
                    await get_external_service_bundle(
                        session, extract_services["JUTE"], mapper, context
                    )
                )

        if len(mappers_bundles) > 0:
            resp.append(await execute_mappers_bundles(client, mappers_bundles))

        return resp
