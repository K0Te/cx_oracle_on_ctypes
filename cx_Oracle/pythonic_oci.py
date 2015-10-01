import ctypes
from ctypes import byref

import oci
from utils import AnythingGoes

def OCIAttrGet(param, oci_function, oci_type, oci_subfunction, environment, context):
    c_result = oci_type()
    arg3 = oci.POINTER(oci.ub4)() # TODO: move somewhere where it is evaluated only once
    status = oci.OCIAttrGet(param, oci_function, byref(c_result), arg3, oci_subfunction, environment.error_handle)
    environment.check_for_error(status, context)
    return c_result.value

def OCIParamGet(handle, htype, environment, pos, context):
    # cant pass cast_param to OCI and return non-cast param. ctypes doesn't know the cast param and the non-cast param are the same.
    param_type = oci.POINTER(oci.OCIParam)
    param = ctypes.c_void_p()
    # acquire parameter descriptor
    status = oci.OCIParamGet(handle, htype, environment.error_handle,
                             byref(param), pos)
    environment.check_for_error(status, context)
    
    result = ctypes.cast(param, param_type)
    return result

def OCIHandleAlloc(environment, handle, handle_type, error_message):
    WrappedOCIHandleAlloc = oci.OCIHandleAlloc
    original_argtypes = oci.OCIHandleAlloc.argtypes
    WrappedOCIHandleAlloc.argtypes = [original_argtypes[0], AnythingGoes()] + original_argtypes[2:]
    argtypes = WrappedOCIHandleAlloc.argtypes
    status = WrappedOCIHandleAlloc(environment.handle, byref(handle), handle_type, 0, argtypes[4]())
    environment.check_for_error(status, error_message)