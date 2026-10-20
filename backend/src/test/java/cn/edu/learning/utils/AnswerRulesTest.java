package cn.edu.learning.utils;
import cn.edu.learning.exception.ApiException;
import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;
class AnswerRulesTest {
 @Test void everyPermutationPreservesTheCorrectAnswer(){
    List<String> permutations=new ArrayList<>(); permute("","ABCD",permutations);
    assertEquals(24,permutations.size());
    for(String order:permutations)for(String answer:List.of("A","B","C","D","AB","AC","AD","BC","BD","CD","ABC","ABD","ACD","BCD","ABCD")){
        String labels=String.join("",AnswerRules.displayedCorrect(answer,order));
        assertTrue(AnswerRules.correct(labels,order,answer),order+" / "+answer);
    }
 }
 private void permute(String prefix,String rest,List<String> result){if(rest.isEmpty())result.add(prefix);else for(int i=0;i<rest.length();i++)permute(prefix+rest.charAt(i),rest.substring(0,i)+rest.substring(i+1),result);}
 @Test void incompleteMultipleIsWrongAndOrderDoesNotMatter(){
    assertEquals("AB",AnswerRules.normalize(List.of("B","A"),"CADB","MULTIPLE"));
    assertTrue(AnswerRules.correct("AB","CADB","AC"));
    assertFalse(AnswerRules.correct("A","CADB","AC"));assertFalse(AnswerRules.correct(null,"CADB","AC"));
 }
 @Test void rejectsDuplicateAndInvalidOptions(){
    assertThrows(ApiException.class,()->AnswerRules.normalize(List.of("A","A"),"ABCD","MULTIPLE"));
    assertThrows(ApiException.class,()->AnswerRules.normalize(List.of("C"),"AB","JUDGE"));
    assertThrows(ApiException.class,()->AnswerRules.normalize(List.of("A","B"),"ABCD","SINGLE"));
 }
 @Test void thresholdsUseUnroundedValuesAndSampleSize(){
    assertEquals("NO_DATA",AnswerRules.level(0,0,true));assertEquals("INSUFFICIENT",AnswerRules.level(2,2,true));
    assertEquals("REVIEW",AnswerRules.level(3,5,true));assertEquals("GOOD",AnswerRules.level(4,5,true));
    assertEquals("WEAK",AnswerRules.level(5999,10000,true));assertEquals("INSUFFICIENT",AnswerRules.level(0,20,false));
 }
}
