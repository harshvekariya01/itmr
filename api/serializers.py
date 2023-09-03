from rest_framework import serializers
from mainapp.models import *
from datetime import datetime,time

class ProjectListSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = URLDetail
        fields = ["id","status","project_id","unique_id","ip_address","country","created_date","created_time"]

    def get_created_date(self,instance):
        return datetime.strftime(instance.created_date, "%Y-%m-%d")

    def get_created_time(self,instance):
        return time.strftime(instance.created_time, "%H:%M:%S")