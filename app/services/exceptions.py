class RecognitionError(Exception):
    pass

class ImageUnreadableError(RecognitionError):
    pass

class PerfumeNotFoundError(RecognitionError):
    pass

class ServiceError(RecognitionError):
    pass
