import requests


class Pleroma:
    def __init__(self, instance_url, access_token, account_id):
        self.instance_url = instance_url
        self.api_url = f"{instance_url}/api/v1"
        self.access_token = access_token
        self.account_id = account_id

    def delete_status(self, status_id):
        res = requests.delete(f"{self.api_url}/statuses/{status_id}", headers={
            "Authorization": f"Bearer {self.access_token}"
        })

        if not res.ok:
            res.raise_for_status()

        print(f"Deleted status {status_id}")

    def get_statuses(self, account_id=None):
        if account_id == None:
            account_id = self.account_id

        res = requests.get(f"{self.api_url}/accounts/{account_id}/statuses", headers={
            "Authorization": f"Bearer {self.access_token}"
        })

        if not res.ok:
            res.raise_for_status()

        return res.json()

    def upload_media(self, media):
        res = requests.post(
            f"{self.api_url}/media",
            files={
                "file": media
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        if not res.ok:
            res.raise_for_status()

        return res.json()

    def post_status(self, body, sensitive=False, media=None):
        if media is None:
            media = []
        media_ids = []

        if len(media) != 0:
            for file in media:
                attachment = self.upload_media(file)

                media_ids.append(attachment["id"])

        res = requests.post(
            f"{self.api_url}/statuses",
            json={
                "sensitive": sensitive,
                "status": body,
                "content_type": "text/markdown",
                "media_ids": media_ids,
                "visibility": "list:5",
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )

        if not res.ok:
            res.raise_for_status()

        return True
