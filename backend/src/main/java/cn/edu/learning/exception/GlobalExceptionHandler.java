package cn.edu.learning.exception;

import cn.edu.learning.pojo.Models.Result;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.servlet.resource.NoResourceFoundException;

@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger log=LoggerFactory.getLogger(GlobalExceptionHandler.class);
    @ExceptionHandler(ApiException.class)
    ResponseEntity<Result> api(ApiException e) { return ResponseEntity.status(e.status).body(new Result(0,e.getMessage(),null)); }
    @ExceptionHandler(DuplicateKeyException.class)
    ResponseEntity<Result> duplicate() { return api(new ApiException(409,"账号或记录已存在")); }
    @ExceptionHandler({MethodArgumentNotValidException.class,MethodArgumentTypeMismatchException.class,HttpMessageNotReadableException.class,MissingServletRequestParameterException.class})
    ResponseEntity<Result> bad(Exception e) { return api(new ApiException(400,"请求参数不符合要求")); }
    @ExceptionHandler(NoResourceFoundException.class)
    ResponseEntity<Result> missing() { return api(new ApiException(404,"接口不存在")); }
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    ResponseEntity<Result> method() { return api(new ApiException(405,"请求方法不支持")); }
    @ExceptionHandler(Exception.class)
    ResponseEntity<Result> unknown(Exception e) { log.error("Request failed: {}",e.getClass().getSimpleName()); return api(new ApiException(500,"服务器处理失败，请稍后重试")); }
}
