from django.db import models
import json
from django.contrib.auth.models import User
# Create your models here.
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    description = models.TextField()
    internal_links = models.TextField(blank=True, null=True)
    images_without_alt = models.TextField(blank=True, null=True)
    top_keyword = models.TextField(blank=True, null=True)

    def set_top_keyword(self, links):
        self.images_without_alt = json.dumps(links)

    def get_top_keyword(self):
        return json.loads(self.top_keyword) if self.top_keyword else []

    def set_images_without_alt(self, links):
        self.images_without_alt = json.dumps(links)

    def get_images_without_alt(self):
        return json.loads(self.images_without_alt) if self.images_without_alt else []

    def set_internal_links(self, links):
        self.internal_links = json.dumps(links)

    def get_internal_links(self):
        return json.loads(self.internal_links) if self.internal_links else []
    timestamp = models.DateTimeField(auto_now_add=True)