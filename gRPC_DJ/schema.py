from gRPC_Demo.models import Student, Teacher
from graphene_django import DjangoObjectType
import graphene

class TeacherType(DjangoObjectType):
    class Meta:
        model= Teacher
        fields = ('id', 'name')

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ('id', 'name', 'roll_no', 'class_teacher')


class Query(graphene.ObjectType):
    all_students = graphene.List(StudentType)
    teacher_by_name = graphene.Field(TeacherType, name=graphene.String(required=True))

    def resolve_all_students(root, info):
        return Student.objects.select_related('class_teacher').all()
    
    def resolve_teacher_by_name(root, info, name):
        try:
            return Teacher.objects.get(name=name)
        except Teacher.DoesNotExist:
            return None
        
schema = graphene.Schema(query=Query)