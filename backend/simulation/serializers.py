from rest_framework import serializers

class SimulationSerializer(serializers.Serializer):
    start_age           = serializers.IntegerField()
    retirement_age      = serializers.IntegerField()
    end_age             = serializers.IntegerField()
    initial_assets      = serializers.FloatField()
    initial_savings     = serializers.FloatField()
    savings_growth_rate = serializers.FloatField()
    mean_return         = serializers.FloatField()
    annual_expense      = serializers.FloatField()
    n_simulations       = serializers.IntegerField()
    