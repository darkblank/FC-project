from rest_framework import serializers


def phone_number(value):
    value = value.replace('-', '')
    if len(value) not in (10, 11):
        raise serializers.ValidationError('전화번호 길이가 올바르지 않습니다')
    if not value.startswith('0'):
        raise serializers.ValidationError('올바른 번호가 아닙니다')
