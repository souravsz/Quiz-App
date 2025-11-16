from rest_framework.response import Response

class ResponseHandler:

    @staticmethod
    def success(data=None, message="Success", status=200):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status)

    @staticmethod
    def error(error="Something went wrong", status=400):
        return Response({
            "success": False,
            "error": error
        }, status=status)
    
    @staticmethod
    def get_error_message(serializer_errors):
        """Extract clean error message from serializer errors"""
        if isinstance(serializer_errors, dict):
            for field, errors in serializer_errors.items():
                if isinstance(errors, list) and errors:
                    return str(errors[0])
        return "Invalid input data"
