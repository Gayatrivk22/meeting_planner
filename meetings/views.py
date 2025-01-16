from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.forms import modelform_factory

from meetings.models import Meeting, Room, Check

class CheckForm(forms.ModelForm):
    required_amenities = forms.MultipleChoiceField(
        choices=Room.AMENITIES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Required Amenities"
    )

    class Meta:
        model = Check
        fields = ['capacity', 'is_private', 'date', 'start_time', 'end_time', 'required_amenities']


@login_required
def detail(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    return render(request, "meetings/detail.html",
                  {"meeting": meeting})


@login_required
def rooms_list(request):
    return render(request, "meetings/rooms_list.html",
            {"rooms": Room.objects.all()})


MeetingForm = modelform_factory(Meeting, exclude=[])


@login_required
def new(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("welcome")
    else:
        form = MeetingForm()
    return render(request, "meetings/new.html",
                  {"form": form})

@login_required
def check(request):
    if request.method == "POST":
        form = CheckForm(request.POST)
        if form.is_valid():
            check_data = form.cleaned_data
            # Find available rooms using the improved method
            available_rooms = Check.find_available_rooms(
                check_data['date'],
                check_data['start_time'],
                check_data['end_time'],
                check_data['capacity'],
                check_data['is_private'],
                check_data['required_amenities']
            )
            request.session['available_rooms'] = [
                {
                    'name': room.name,
                    'floor': room.floor,
                    'room_number': room.room_number,
                    'capacity': room.capacity,
                    'room_type': room.room_type_display,
                    'amenities': [dict(Room.AMENITIES)[a] for a in room.amenities]
                }
                for room in available_rooms
            ]
            return redirect("display")
    else:
        form = CheckForm()
    return render(request, "meetings/check.html", {"form": form})

@login_required
def display(request):
    available_rooms = request.session.get('available_rooms', [])
    return render(request, "meetings/display.html", {"rooms": available_rooms})


@login_required
def edit(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect("detail", id)
    else:
        form = MeetingForm(instance=meeting)
    return render(request, "meetings/edit.html",
                  {"form": form})


@login_required
def delete(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    if request.method == "POST":
        # Form is only shown to ask for confirmation
        # When we get a POST, we know we can go ahead and delete
        meeting.delete()
        return redirect("welcome")
    else:
        return render(request, "meetings/confirm_delete.html",
                      {"meeting": meeting})
