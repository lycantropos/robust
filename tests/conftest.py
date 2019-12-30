from hypothesis import (HealthCheck,
                        settings)

settings.register_profile('default',
                          deadline=None,
                          suppress_health_check=[HealthCheck.data_too_large,
                                                 HealthCheck.filter_too_much,
                                                 HealthCheck.too_slow])
