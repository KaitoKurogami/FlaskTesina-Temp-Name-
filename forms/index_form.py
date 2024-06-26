from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, widgets,SelectMultipleField,IntegerField,FormField, DecimalField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileAllowed
import decimal
from wtforms.fields import TextAreaField
from wtforms.widgets import TextArea

class BetterDecimalField(DecimalField):
    """
    Very similar to WTForms DecimalField, except with the option of rounding
    the data always.
    """
    def __init__(self, label=None, validators=None, places=2, rounding=None,
                 round_always=False, **kwargs):
        super(BetterDecimalField, self).__init__(
            label=label, validators=validators, places=places, rounding=
            rounding, **kwargs)
        self.round_always = round_always

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(valuelist[0])
                if self.round_always and hasattr(self.data, 'quantize'):
                    exp = decimal.Decimal('.1') ** self.places
                    if self.rounding is None:
                        quantized = self.data.quantize(exp)
                    else:
                        quantized = self.data.quantize(
                            exp, rounding=self.rounding)
                    self.data = quantized
            except (decimal.InvalidOperation, ValueError):
                self.data = None
                raise ValueError(self.gettext('Not a valid decimal value'))

class UploadFileForm(FlaskForm):
    file = FileField(label="Imagen, 'jpeg', 'jpg', 'png' o 'webp'", validators=[InputRequired(),FileAllowed(['jpg', 'jpeg', 'png','webp'])])
    #submit = SubmitField("Confirm File")

class UploadNetForm(FlaskForm):
    newNet = FileField(label="Seleccione la red. Debe ser 'h5'", validators=[FileAllowed(['h5'])],render_kw={'disabled':'true'})

class ClassesForm(FlaskForm):
    classesText = TextAreaField(label="Escriba las categorias, separadas por coma:",render_kw={'disabled':'true',"rows": 4, "cols": 30})

class SHAPForm(FlaskForm):
    SHAP_evals=IntegerField("Evaluations",description="1000 por defecto",default=1000, validators=[DataRequired()],render_kw={'disabled':'true'})
    SHAP_batch_size=IntegerField("Batch size", validators=[DataRequired()],default=10,render_kw={'disabled':'true'})
    
class LIMEForm(FlaskForm):
    LIME_perturbations=IntegerField("Perturbations",default=500, validators=[DataRequired()],render_kw={'disabled':'true'})
    LIME_kernel_size=BetterDecimalField(label="Kernel Size", validators=[DataRequired()],round_always=True,default=2.5,render_kw={'disabled':'true'})
    LIME_max_dist=BetterDecimalField(label="Maximum distance of perturbations", validators=[DataRequired()],round_always=True,default=28,render_kw={'disabled':'true'})
    LIME_ratio=BetterDecimalField(label="Ratio of perturbations", validators=[DataRequired()],round_always=True,default=0.3,render_kw={'disabled':'true'})

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FullForm(FlaskForm):
    string_of_nets = ['VGG16,ResNet50,Red propia']
    list_of_nets = string_of_nets[0].split(",")
    # create a list of value/description tuples
    nets = [(x, x) for x in list_of_nets]
    nets = MultiCheckboxField(label='nets', choices=nets,render_kw={'class':'checkboxNets'})
    file = FormField(UploadFileForm)
    newNet = FormField(UploadNetForm)
    shap = FormField(SHAPForm)
    lime = FormField(LIMEForm)
    classesText = FormField(ClassesForm)
    submit=SubmitField(label="Procesar Imagen",render_kw={'disabled':'true'})