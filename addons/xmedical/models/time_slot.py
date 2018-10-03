# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Laxicon Solution.
#    (<http://laxicon.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import api, fields, models
from datetime import datetime, timedelta
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


DAY_TIME_SELECTION = [
    (1, '1'), (2, '2'), (3, '3'), (4, '4'),
    (5, '5'), (6, '6'), (7, '7'), (8, '8'),
    (9, '9'), (10, '10'), (11, '11'), (12, '12'),
    (13, '13'), (14, '14'), (15, '15'), (16, '16'),
    (17, '17'), (18, '18'), (19, '19'), (20, '20'),
    (21, '21'), (22, '22'), (23, '23'), (24, '24')
    ]


class TimeSlot(models.Model):
    _name = "time.slot.management"
    _inherit = ['mail.thread']

    name = fields.Many2one('res.partner', string="Doctor", required=True)
    day = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], string="Day")
    monday_slot_ids = fields.One2many('time.slot.line', 'monday_time_slot_id', string="Monday Slot")
    tuesday_slot_ids = fields.One2many('time.slot.line', 'tuesday_time_slot_id', string="Tuesday Slot")
    wednesday_slot_ids = fields.One2many('time.slot.line', 'wednesday_time_slot_id', string="Wednesday Slot")
    thursday_slot_ids = fields.One2many('time.slot.line', 'thursday_time_slot_id', string="Thursday Slot")
    friday_slot_ids = fields.One2many('time.slot.line', 'friday_time_slot_id', string="Friday Slot")
    saturday_slot_ids = fields.One2many('time.slot.line', 'saturday_time_slot_id', string="Saturday Slot")
    sunday_slot_ids = fields.One2many('time.slot.line', 'sunday_time_slot_id', string="Sunday Slot")
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")

    @api.multi
    def set_time_slot(self):
        if self.day:
            time_line_obj = self.env['time.slot.line']
            time_list = self.set_time_slot_duration(self.start_time, self.end_time)
            if self.day == 'monday':
                print ("monday")
                self._cr.execute("delete from time_slot_line where monday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'monday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'tuesday':
                print ("tuesday")
                self._cr.execute("delete from time_slot_line where tuesday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'tuesday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'wednesday':
                print ("wednesday")
                self._cr.execute("delete from time_slot_line where wednesday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'wednesday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'thursday':
                print ("thursday")
                self._cr.execute("delete from time_slot_line where thursday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'thursday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'friday':
                print ("friday")
                self._cr.execute("delete from time_slot_line where friday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'friday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'saturday':
                print ("saturday")
                self._cr.execute("delete from time_slot_line where saturday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'saturday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)
            if self.day == 'sunday':
                print ("sunday")
                self._cr.execute("delete from time_slot_line where sunday_time_slot_id = %s" % (self.id))
                for t in time_list:
                    data = {
                        'sunday_time_slot_id': self.id,
                        'start_time': t.get('start_time'),
                        'end_time': t.get('end_time')
                    }
                    time_line_obj.create(data)

    def set_time_slot_duration(self, start=None, end=None):
        # tz = pytz.timezone(self.env.user.partner_id.tz)
        # start = fields.datetime.now()
        start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        print (">>>>>>>>>>>>>>>>>>>>1", start_time)

        # start_time = start.replace(hour=self.start_time, minute=00, second=00).strftime('%Y-%m-%d %H:%M:%S')
        # end_time = start.replace(hour=self.end_time, minute=00, second=00).strftime('%Y-%m-%d %H:%M:%S')
        time_list = []
        print (">>>>>>>>>>>>>>>>>>>>2", start_time)
        while start_time < end_time:
            # start_time = pytz.utc.localize(datetime.strptime(start, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
            # end_time = pytz.utc.localize(datetime.strptime(end, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
            end = start_time + timedelta(minutes=30)
            data = {
                'start_time': start_time.time(),
                'end_time': end.time()
            }
            time_list.append(data)
            start_time = start_time + timedelta(minutes=30)
        return time_list


class TimeSlotLine(models.Model):
    _name = "time.slot.line"
    _rec_name = "start_time"

    monday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    tuesday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    wednesday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    thursday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    friday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    saturday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    sunday_time_slot_id = fields.Many2one('time.slot.management', string="Time slot Master Monday")
    start_time = fields.Char(string="Start Time")
    end_time = fields.Char(string="End time")
