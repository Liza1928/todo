from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tasks(models.Model):

    id = fields.IntField(pk=True)
    text = fields.TextField(null=False)
    repeat = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"

    def __str__(self):
        return self.text

    @classmethod
    def get_all(cls):
        return cls.all()


Task_Pydantic = pydantic_model_creator(Tasks, name="Tasks")
TaskIn_Pydantic = pydantic_model_creator(Tasks, name="TasksIn", exclude_readonly=True)