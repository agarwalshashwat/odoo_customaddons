from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class SchoolStudentModel(models.Model):
    _name = "school.student"
    # _description = "School students data"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("new","New"),("current","Current"),("passout","Pass Out")], string="State",default="new")
    course_id = fields.Many2one(comodel_name="school.course",relation="student_course_relation",column1="studentid",column2="courseid", string = "Course ID")
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="student_subject_relation",column1="studentid",column2="subjectid", string = "Subject IDs")
    student_course = fields.One2many("school.course",inverse_name="student_ids")

    def action_new(self):
        self.state = "new"

    def action_passout(self):
        self.state = "passout"

    def action_current(self):
        self.state = "current"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            # _logger.info("===========Search-----%r-------",rec.date_of_birth)
            # today = datetime.date.today()
            # dob = rec.date_of_birth
            if rec.date_of_birth:
                # _logger.info("===========Search-----%r---%r----",date.today().year -  rec.date_of_birth.year.year, rec.date_of_birth)
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    @api.constrains("course_id")
    def studentcourseids(self):
        for rec in self:
            _logger.info("===========Search-----%r----",rec.course_id.id)
            obj = self.env['school.course'].search([("id","=",rec.course_id.id)]).create({
                "student_name" : self.name,
            })
            
        

class SchoolTeacherModel(models.Model):
    _name = "school.teacher"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(compute = "AgeCalculator",string = "Age")
    gender = fields.Selection([("m","Male"),("f","Female")], string="Gender")
    image = fields.Binary(string="Image")
    email = fields.Char(string="E-mail")
    phone = fields.Char(string="Phone", size=10)
    registration_number = fields.Char(string="Registration Number")
    date_registration = fields.Date(string = "Date of Registration")
    street = fields.Text(string="Street")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state",string="State ID")
    country_id = fields.Many2one("res.country",string = "Country ID")
    zip = fields.Char(string="Zip", size=6)
    state = fields.Selection([("active","Active"),("inactive","Inactive")], string="State")
    course_ids = fields.Many2many(comodel_name="school.course",relation="teacher_course_relation",column1="teacherid",column2="courseid", string = "Course IDs")
    subject_ids = fields.Many2many(comodel_name="school.subject",relation="teacher_subject_relation",column1="teacherid",column2="subjectid", string = "Subject IDs")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")
    teacher_course = fields.Many2one("school.course",string="Teacher IDs")

    def action_active(self):
        self.state = "active"

    def action_inactive(self):
        self.state = "inactive"

    @api.depends("date_of_birth")
    def AgeCalculator(self):
        for rec in self:
            rec.age = 0
            if rec.date_of_birth:
                rec.write({
                    "age": date.today().year -  rec.date_of_birth.year,
                })

    # @api.constrains("course_ids")
    # def teachercourseids(self):
    #     for rec in self:
    #         _logger.info("===========Search-----%r------",type(rec.course_ids))

class SchoolCourseModel(models.Model):
    _name = "school.course"
    _rec_name = "name"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    duration = fields.Integer(string="Duration")
    fee = fields.Integer(string="Fee")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")
    position = fields.Char(string="Position/Designation")
    # teacher_ids = fields.One2many("school.teacher",inverse_name="teacher_course")
    student_ids = fields.Many2many("school.student", string="Student IDs")
    student_name = fields.Char("Student's Name")
    # teacher_name = fields.Char(string="Teacher IDs")

    # @api.depends("teacher_ids")
    # def _teachercourse_(self):
    #     for rec in self:
    #         _logger.info("===========Search-----%r------",rec.teacher_ids.course_ids)
    #         for course in rec.teacher_ids:
    #             _logger.info("===========Search-----%r------",course.course_ids)
    #             if rec.id == course.course_ids:
    #                 rec.write({
    #                     "teacher_name" : course.name,
    #                 })

    # @api.depends("student_ids")
    # def _studentcourse_(self):
    #     for rec in self:
    #         for course in rec.student_ids:
    #             _logger.info("===========Search-----%r------",course.course_id)
    #             if rec.id == course.course_id:
    #                 rec.write({
    #                     "student_name": course.name
    #                 })


class SchoolSubjectModel(models.Model):
    _name = "school.subject"
    _rec_name = "name"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    department = fields.Selection([("photo","Photography"),("softdev","Software Development"),("webdev","Web Development")], string="Department")

class SchoolFeesModel(models.Model):
    _name = "school.fee"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student",string="Student ID")
    total_fee = fields.Float(string="Total Fees")
    due_fee = fields.Float(compute = "DuesCalculator", string="Due Fees")
    amount_paid = fields.Float(string="Amount Paid")
    course_id = fields.Many2one("school.course",string="Course ID")

    # @api.depends(course_id)
    # def TotalFee(self):
    #     for rec in self:
    #         rec.total_fee = 0
    #         if 

    @api.depends("total_fee","amount_paid")
    def DuesCalculator(self):
        for rec in self:
            rec.due_fee = 0
            if rec.total_fee and rec.amount_paid:
                rec.write({
                    "due_fee" : rec.total_fee - rec.amount_paid,
                })

    def action_register_payment(self):
        return{
            "name":("Register Payment"),
            "view_mode":"form",
            "res_model":"school.fee.wizard",
            "type":"ir.actions.act_window",
            "target":"new",
        }

class SchoolFeeLineModel(models.Model):
    _name="school.fee.line"
    _rec_name = "student_id"

    student_id = fields.Many2one("school.student",string="Student ID",required=True)
    due_fee = fields.Float(string="Due Fees")
    amount_paid = fields.Float(string="Amount Paid")    