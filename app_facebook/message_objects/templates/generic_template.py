from typing import List
from app_facebook.message_objects.elements.element import Element
from app_facebook.message_objects.templates.base_template import BaseTemplate
from app_facebook.message_objects.templates.template_type_enum import TemplateTypeEnum


class GenericTemplate(BaseTemplate):
    def __init__(self, elements: List[Element]):
        super().__init__()

        self.elements = elements
        self.template_type = TemplateTypeEnum.GENERIC.value

    def to_json(self):
        json = super().to_json()
        json['elements'] = [element.to_json() for element in self.elements]
        return json
