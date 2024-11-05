from django import forms
from .models import Quiz, QuizQuestion, QuizOption,User,DiscussionForum
from .models import QuizResponse,Feedback

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course', 'quiz_title', 'max_marks', 'duration']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['quiz','question_text', 'question_type', 'max_marks']
        
def __init__(self, *args, **kwargs):
        
        self.question = kwargs.pop('question', None)  
        super().__init__(*args, **kwargs)
        if self.question is not None:
            self.fields['question_text'].initial = self.question.question_text
            self.fields['question_type'].initial = self.question.question_type
            self.fields['max_marks'].initial = self.question.max_marks        

class QuizOptionForm(forms.ModelForm):
    class Meta:
        model = QuizOption
        fields = ['option_no', 'option_text', 'is_correct','question']


class QuizResponseForm(forms.ModelForm):
    class Meta:
        model = QuizResponse
        fields = ['selected_option'] 
        widgets = {
            'selected_option': forms.RadioSelect(),  
        }

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizResponse
        fields = ['selected_option']  
     

class UserProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']     


class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message...', 'class': 'form-control'}))
    
    class Meta:
        model = DiscussionForum
        fields = ['content','course']        



class FeedbackForm(forms.ModelForm):
    content = forms.CharField(label='Your Feedback',widget=forms.Textarea(attrs={'rows': 6, 'cols': 42}))
    class Meta:
        model=Feedback
        fields=['content']