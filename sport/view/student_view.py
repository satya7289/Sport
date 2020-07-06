import datetime as D
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q

from sport.models import Sport
from sport.models import Student


class StudentListView(View):
    template_name = "student/Students.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        return self.pagination(students)

    def pagination(self, object):
        paginator = Paginator(object, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        return render(self.request, self.template_name, {"students": students})


class StudentCreateView(View):
    template_name = "student/CreateStudent.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            first_name = request.POST.get("first-name")
            last_name = request.POST.get("last-name")
            roll_no = request.POST.get("roll-no")
            email = request.POST.get("email")
            team = request.POST.get("sport-name")

            # print(first_name,last_name,roll_no,email,team)
            # Get sport by team name
            if team:
                sport = Sport.objects.filter(name=team).first()
                if Student.objects.filter(roll_no=roll_no):
                    messages.error(request, "Roll No Already Exits.")
                    return render(request, self.template_name)
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    roll_no=roll_no,
                    email=email,
                    created_at=D.datetime.now().date(),
                )
                student.save()
                sport.student_set.add(student)
                print(first_name, last_name, roll_no, email, team, sport)
                return redirect("students")
            messages.error(request, "Enter Sport Name")
            return render(request, self.template_name)


class EditStudentView(View):
    template_name = "student/EditStudent.html"

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            id = request.GET.get("id")
            try:
                student = Student.objects.get(id=id)
                return render(
                    request,
                    self.template_name,
                    {"student": student, "sport": student.team.first()},
                )
            except Student.DoesNotExist:
                raise Http404

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            first_name = request.POST.get("first-name")
            last_name = request.POST.get("last-name")
            email = request.POST.get("email")
            team = request.POST.get("sport-name")
            id = request.GET.get("id")
            try:
                student = Student.objects.get(id=id)
                student.first_name = first_name
                student.last_name = last_name
                student.email = email
                student.save()
                try:
                    new_team = Sport.objects.get(name=team)
                    prev_team = student.team.first()
                    if not team == str(prev_team):
                        student.team.remove(prev_team)
                        student.team.add(new_team)
                    return redirect("students")

                except Sport.DoesNotExist:
                    raise Http404
            except Student.DoesNotExist:
                raise Http404


class SearchStudentView(View):
    template_name = "student/Students.html"

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("q", "")
        search_type = request.GET.get("type", "")
        if search_type == "Name":
            students = Student.objects.filter(
                Q(first_name__contains=search_query)
                | Q(last_name__contains=search_query)
            )
        elif search_type == "RollNo":
            students = Student.objects.filter(Q(roll_no__contains=search_query))
        elif search_type == "Email":
            students = Student.objects.filter(Q(email__contains=search_query))
        elif search_type == "All":
            students = Student.objects.filter(
                Q(first_name__contains=search_query)
                | Q(last_name__contains=search_query)
                | Q(email__contains=search_query)
            )
        return render(
            request, self.template_name, {"students": students, "q": search_query}
        )
