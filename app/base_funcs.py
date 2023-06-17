from app import session, PSYCHO_SITE_REST_URL


async def send_psycho_site_request(method, url, return_json=True, raise_if_not_ok=False, **kwargs):
    async with session.request(method=method, url=f'{PSYCHO_SITE_REST_URL}/{url}', **kwargs) as response:
        if not response.ok:
            if raise_if_not_ok and response.status != 404:
                raise RuntimeError(f'Failed to send {method} to psycho site (URl={url}): {await response.text()}')
            return_value = None
        else:
            return_value = (await response.json()) if return_json else None
        return response.status, return_value
