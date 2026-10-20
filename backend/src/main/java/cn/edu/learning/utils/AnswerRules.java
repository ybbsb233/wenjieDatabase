package cn.edu.learning.utils;

import cn.edu.learning.exception.ApiException;
import cn.edu.learning.pojo.Models.*;
import java.util.*;

/** The mapping is stored once per exercise item; the client only submits displayed labels. */
public final class AnswerRules {
    private AnswerRules() {}
    public static String shuffle(String type) {
        if("JUDGE".equals(type)) return "AB";
        List<String> labels=new ArrayList<>(List.of("A","B","C","D")); Collections.shuffle(labels);
        return String.join("",labels);
    }
    public static List<Option> options(Question q,String order) {
        List<Option> result=new ArrayList<>();
        for(int i=0;i<order.length();i++) {
            String text=switch(order.charAt(i)) { case 'A'->q.optionA(); case 'B'->q.optionB(); case 'C'->q.optionC(); case 'D'->q.optionD(); default->throw new IllegalStateException("Invalid saved mapping"); };
            result.add(new Option(String.valueOf((char)('A'+i)),text));
        }
        return result;
    }
    public static String normalize(List<String> labels,String order,String type) {
        if(labels==null) throw new ApiException(400,"答案不能为空对象");
        Set<String> unique=new TreeSet<>();
        for(String label:labels) {
            if(label==null||label.length()!=1||label.charAt(0)<'A'||label.charAt(0)>='A'+order.length()||!unique.add(label)) throw new ApiException(400,"选项不合法或重复");
        }
        if(!"MULTIPLE".equals(type)&&unique.size()>1) throw new ApiException(400,"单选或判断只能选择一项");
        return unique.isEmpty()?null:String.join("",unique);
    }
    public static boolean correct(String selected,String order,String original) {
        if(selected==null) return false;
        StringBuilder mapped=new StringBuilder(); for(char c:selected.toCharArray()) mapped.append(order.charAt(c-'A'));
        char[] chars=mapped.toString().toCharArray(); Arrays.sort(chars); return original.equals(new String(chars));
    }
    public static List<String> displayedCorrect(String original,String order) {
        List<String> labels=new ArrayList<>(); for(int i=0;i<order.length();i++) if(original.indexOf(order.charAt(i))>=0) labels.add(String.valueOf((char)('A'+i))); return labels;
    }
    public static List<String> labels(String value) { return value==null?List.of():value.chars().mapToObj(c->String.valueOf((char)c)).toList(); }
    public static Double accuracy(long correct,long count) { return count==0?null:Math.round(correct*1000.0/count)/10.0; }
    public static String level(long correct,long count,boolean sufficientPeople) {
        if(count==0) return "NO_DATA"; if(count<3||!sufficientPeople) return "INSUFFICIENT";
        double ratio=(double)correct/count; return ratio<0.6?"WEAK":ratio<0.8?"REVIEW":"GOOD";
    }
}
