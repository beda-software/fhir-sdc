import itertools

from aiohttp import ClientSession, web


async def external_service_extraction(client, service, template, context):
    async with ClientSession() as session:
        async with session.post(
            service,
            json={
                "template": template,
                "context": context,
            },
        ) as result:
            if 200 <= result.status <= 299:
                bundle = await result.json()
                return await client.execute("/", data=bundle)
            else:
                raise web.HTTPBadRequest(body=await result.text())


async def execute_jute_mappers_bundles(client, mappers_bundles):
    not_transaction = any(bundle.get("type") != "transaction" for bundle in mappers_bundles)

    result_bundle = {
        "resourceType": "Bundle",
        "type": "batch" if not_transaction else "transaction",
        "entry": list(itertools.chain.from_iterable(bundle["entry"] for bundle in mappers_bundles)),
    }

    return await client.execute("/", data=result_bundle)


async def extract(client, mappings, context, extract_services):
    """
    mappings could be a list of Aidbox Mapping resources
    or plain jute templates
    """
    resp = []
    jute_mappers_bundles = []

    for mapper in mappings:
        if "resourceType" in mapper and "body" in mapper:
            # It is custome mapper resource
            mapper_type = mapper.get("type", "JUTE")
            if mapper_type == "JUTE" and extract_services["JUTE"] == "aidbox":
                mapper_bundle = await mapper.execute("$debug", data=context)
                if "entry" not in mapper_bundle:
                    continue

                jute_mappers_bundles.append(mapper_bundle)
            else:
                # Use 3rd party service FHIRPathMapping or JUTE
                resp.append(
                    await external_service_extraction(
                        client, extract_services[mapper_type], mapper["body"], context
                    )
                )
        else:
            # legacy extraction
            resp.append(
                await external_service_extraction(client, extract_services["JUTE"], mapper, context)
            )

    if len(jute_mappers_bundles) > 0:
        resp.append(await execute_jute_mappers_bundles(client, jute_mappers_bundles))

    return resp
