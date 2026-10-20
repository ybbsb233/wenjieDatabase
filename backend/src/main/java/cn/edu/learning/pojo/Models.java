package cn.edu.learning.pojo;

import java.time.LocalDateTime;
import java.util.List;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;

/** Immutable database rows and explicit request/response objects. IDs are strings at the API boundary. */
public final class Models {
    private Models() {}
    public record User(Long id, String username, String realName, String passwordHash, String role,
                       Integer enabled, Integer mustChangePassword, Long tokenVersion, LocalDateTime createdAt) {}
    public record UserView(String id, String username, String realName, String role, boolean enabled,
                           boolean mustChangePassword, LocalDateTime createdAt) {
        public static UserView from(User u) { return new UserView(u.id().toString(),u.username(),u.realName(),u.role(),u.enabled()==1,u.mustChangePassword()==1,u.createdAt()); }
    }
    public record Question(Long id, Long chapterId, Long courseId, String questionType, String stem,
                           String optionA, String optionB, String optionC, String optionD, String correctAnswer, String explanation) {}
    public record Practice(Long id, Long studentId, Long courseId, Long chapterId, String sourceType, String status,
                           Integer questionCount, Integer correctCount, LocalDateTime startedAt, LocalDateTime submittedAt) {}
    public record Item(Long id, Long practiceId, Long questionId, Integer orderNo, String optionOrder,
                       String selectedAnswer, Integer isCorrect) {}
    public record Login(@NotBlank @Size(max=32) String username, @NotBlank @Size(max=72) String password) {}
    public record Password(@NotBlank String oldPassword, @NotBlank @Size(min=6,max=72) String newPassword) {}
    public record NewStudent(@NotBlank @Pattern(regexp="[0-9]{1,32}") String username,
                             @NotBlank @Size(max=50) String realName) {}
    public record Status(@NotNull Boolean enabled) {}
    public record Start(@NotBlank String courseId, String chapterId, String knowledgeId, @Min(1) @Max(50) int count) {}
    public record WrongStart(@NotBlank String courseId, @NotEmpty @Size(max=50) List<@NotBlank String> questionIds) {}
    public record Answer(@NotBlank String itemId, @NotNull @Size(max=4) List<@Pattern(regexp="[A-D]") String> selectedLabels) {}
    public record Submit(@NotNull @Size(max=50) List<@Valid Answer> answers) {}
    public record Option(String label, String text) {}
    public record QuestionView(String itemId, int orderNo, String questionType, String stem, List<Option> options) {}
    public record ResultItem(String itemId, String questionId, int orderNo, String questionType, String stem,
                             List<Option> options, List<String> selectedLabels, List<String> correctLabels,
                             boolean isCorrect, String explanation) {}
    public record Page<T>(long total, List<T> rows) {}
    public record Result(int code, String msg, Object data) {
        public static Result ok(Object data) { return new Result(1,"success",data); }
    }
}
