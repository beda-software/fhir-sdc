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


async def extract(client, mappings, context, extract_services):
    """
    mappings could be a list of Aidbox Mapping resources
    or plain jute templates
    """
    resp = []

    for mapper in mappings:
        if "resourceType" in mapper and "body" in mapper:
            # It is custome mapper resource
            mapper_type = mapper.get("type", "JUTE")
            if mapper_type == "JUTE" and extract_services["JUTE"] == "aidbox":
                # Aidbox native extraction
                resp.append(await mapper.execute("$apply", data=context))
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

    return resp
