from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.response import Response

from core.permissions import ROLE_POLICY_RECORDS, RolePermission
from records.models import Record
from records.serializers import RecordSerializer
from records.services import (
    create_record,
    delete_record,
    list_records,
    parse_record_filters,
    update_record,
)




class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    
    serializer_class = RecordSerializer
    permission_classes = [RolePermission]
    role_policy = ROLE_POLICY_RECORDS

    def get_queryset(self):
        filters = parse_record_filters(query_params=self.request.query_params)
        return list_records(requesting_user=self.request.user, filters=filters)

    # def perform_create(self, serializer):
    #     record = create_record(requesting_user=self.request.user, payload=serializer.validated_data)
    #     serializer.instance = record 

    def perform_create(self, serializer):
        record = create_record(
            requesting_user=self.request.user,
            payload=serializer.validated_data
        )
        serializer.instance = record


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated = update_record(record=instance, payload=serializer.validated_data)
        out = self.get_serializer(updated)
        return Response(out.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_record(record=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
