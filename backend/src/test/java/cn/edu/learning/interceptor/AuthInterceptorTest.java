package cn.edu.learning.interceptor;

import cn.edu.learning.exception.ApiException;
import cn.edu.learning.pojo.Models.User;
import cn.edu.learning.service.AuthService;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class AuthInterceptorTest {
    @Test void defaultPasswordFlagDoesNotBlockLearningButAdminRoleStillRequired() {
        AuthService auth=mock(AuthService.class);
        User student=new User(20L,"20240020","罗晴","unused","STUDENT",1,1,0L,null);
        when(auth.verify("test-token")).thenReturn(student);
        AuthInterceptor interceptor=new AuthInterceptor(auth);
        MockHttpServletRequest request=new MockHttpServletRequest("GET","/api/student/summary");
        request.addHeader("Authorization","Bearer test-token");
        assertTrue(interceptor.preHandle(request,new MockHttpServletResponse(),new Object()));
        request.setRequestURI("/api/admin/students");
        ApiException denied=assertThrows(ApiException.class,()->interceptor.preHandle(request,new MockHttpServletResponse(),new Object()));
        assertEquals(403,denied.status);
    }
}
