fcViews.agenda = {
    'class': AgendaView,
    defaults: {
        allDaySlot: true,
        slotDuration: '00:30:00',
        minTime: '10:00:00',
        maxTime: '20:00:00',
        slotEventOverlap: true, // a bad name. confused with overlap/constraint system
        slotMinutes: '00:30:00',
        axisFormat: 'h(:mm)tt',
        timeFormat: {agenda: 'h:mm{ - h:mm}'},
        dragOpacity: {agenda: '.5'},
        defaultEventMinutes: '120',
        firstHour: '10:00:00',
        allDayText: 'all-day',
    }
};
