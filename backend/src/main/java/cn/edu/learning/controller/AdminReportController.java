package cn.edu.learning.controller;
import cn.edu.learning.pojo.Models.*;
import cn.edu.learning.service.*;
import cn.edu.learning.utils.Ids;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController @RequestMapping("/api/admin")
public class AdminReportController {
 private final LearningService learning;private final StudentService students;private final PracticeService practices;
 public AdminReportController(LearningService l,StudentService s,PracticeService p){learning=l;students=s;practices=p;}
 @GetMapping("/summary") public Result summary(){return Result.ok(Map.of("students",students.counts(),"courses",learning.summary(null)));}
 @GetMapping("/knowledge-analysis") public Result analysis(@RequestParam String courseId){return Result.ok(learning.knowledge(null,Ids.parse(courseId)));}
 @GetMapping("/course-students") public Result courseStudents(@RequestParam String courseId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){return Result.ok(learning.courseStudents(Ids.parse(courseId),page,pageSize));}
 @GetMapping("/students/{id}/summary") public Result studentSummary(@PathVariable String id){long s=student(id);return Result.ok(learning.summary(s));}
 @GetMapping("/students/{id}/knowledge-analysis") public Result studentAnalysis(@PathVariable String id,@RequestParam String courseId){long s=student(id);return Result.ok(learning.knowledge(s,Ids.parse(courseId)));}
 @GetMapping("/students/{id}/trend") public Result trend(@PathVariable String id,@RequestParam String courseId){long s=student(id);return Result.ok(learning.trend(s,Ids.parse(courseId)));}
 @GetMapping("/students/{id}/practices") public Result history(@PathVariable String id,@RequestParam(required=false) String courseId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){long s=student(id);return Result.ok(practices.history(s,Ids.optional(courseId),page,pageSize));}
 @GetMapping("/students/{id}/wrong-questions") public Result wrong(@PathVariable String id,@RequestParam(required=false) String courseId,@RequestParam(required=false) String knowledgeId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){long s=student(id);return Result.ok(learning.wrong(s,Ids.optional(courseId),Ids.optional(knowledgeId),page,pageSize));}
 @GetMapping("/practices/{id}/result") public Result result(@RequestAttribute("currentUser") User u,@PathVariable String id){return Result.ok(practices.result(u,Ids.parse(id)));}
 @GetMapping("/practices") public Result allHistory(@RequestParam(required=false) String studentId,@RequestParam(required=false) String courseId,@RequestParam(defaultValue="1") int page,@RequestParam(defaultValue="10") int pageSize){Long id=Ids.optional(studentId);if(id!=null)students.student(id);return Result.ok(practices.allHistory(id,Ids.optional(courseId),page,pageSize));}
 private long student(String id){long s=Ids.parse(id);students.student(s);return s;}
}
