import os
import requests


class Pleroma():
    def __init__(self, instance_url, access_token, account_id):
        self.instance_url = instance_url
        self.api_url = f"{instance_url}/api/v1"
        self.access_token = access_token
        self.account_id = account_id

    def delete_status(self, id):
        res = requests.delete(f"{self.api_url}/statuses/{id}", headers={
            "Authorization": f"Bearer {self.access_token}"
        })

        if not res.ok:
            res.raise_for_status()

        print(f"Deleted status {id}")

    def purge(self, num_posts=-1):
        res = requests.get(f"{self.api_url}/accounts/{self.account_id}/statuses")

        if not res.ok:
            res.raise_for_status()

        for status in res.json()[:num_posts]:
            self.delete_status(status["id"])

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

    def post_status(self, body, sensitive=False, media=[]):
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
