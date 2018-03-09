from flask_wtf import FlaskForm
from wtforms import \
    StringField,\
    TextField,\
    PasswordField,\
    BooleanField,\
    SubmitField,\
    SelectField

from wtforms.validators import \
    DataRequired,\
    Required,\
    IPAddress,\
    Length,\
    EqualTo,\
    NumberRange,\
    Optional

from wtforms import \
    IntegerField,\
    validators

class LANConfiguration(FlaskForm):
    my_choices = [('1', 'Static IP'), ('2', 'Dynamic IP (DHCP)')]
    ip_mode = SelectField('IP Mode',choices = my_choices)
    ip_address  = StringField(u'IP Address', validators=[IPAddress()])
    subnet_mask  = StringField(u'Subnet Mask', validators=[IPAddress()])
    #default_gateway_address  = StringField(u'Default Gateway Address', validators=[IPAddress(),Optional()])
    #primary_dns_ip_address  = StringField(u'Primary DNS IP Address', validators=[IPAddress(),Optional()])
    #secondary_dns_ip_address  = StringField(u'Secondary DNS IP Address', validators=[IPAddress(),Optional()])
    default_gateway_address  = StringField(u'Default Gateway Address', validators=[IPAddress()])
    primary_dns_ip_address  = StringField(u'Primary DNS IP Address', validators=[IPAddress()])
    secondary_dns_ip_address  = StringField(u'Secondary DNS IP Address', validators=[IPAddress()])
    submit = SubmitField('Update')
