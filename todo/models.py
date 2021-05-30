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


Task_Pydantic = pydantic_model_creator(Tasks, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Tasks, name="TaskIn", exclude_readonly=True)