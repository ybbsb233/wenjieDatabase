package cn.edu.learning.utils;
import cn.edu.learning.exception.ApiException;
public final class Ids {
    private Ids() {}
    public static long parse(String id) {
        try { long value=Long.parseLong(id); if(value<=0) throw new NumberFormatException(); return value; }
        catch (Exception e) { throw new ApiException(400,"编号必须为正整数"); }
    }
    public static Long optional(String id) { return id==null||id.isBlank()?null:parse(id); }
    public static int offset(int page,int size) {
        if(page<1||size<1||size>50||page>1000000) throw new ApiException(400,"分页参数不合法");
        return (page-1)*size;
    }
}
