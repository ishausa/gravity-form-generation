#!/usr/bin/python

__author__ = 'prasanna.venkatasubramanian'

import sys
import os
from string import Template

SINGLE_VENUE_TEMPLATE_FILENAMES = ["templates/TeacherLedIE_WoB_SingleVenue_Template.xml",
                                   "templates/TeacherLedIE_WoB_VolCredit_SingleVenue_Template.xml",
                                   "templates/TeacherLedIE_WoB_VolOffline_SingleVenue_Template.xml"]
TWO_VENUES_TEMPLATE_FILENAMES = ["templates/TeacherLedIE_WoB_TwoVenues_Template.xml",
                                 "templates/TeacherLedIE_WoB_VolCredit_TwoVenues_Template.xml",
                                 "templates/TeacherLedIE_WoB_VolOffline_TwoVenues_Template.xml"]
TEMPLATES_FOLDER = "templates"
GENERATED_FORMS_FOLDER = "generated-forms"
CITY_PROPERTY_NAME = "city"
SECOND_VENUE_PROPERTY_NAME = "venue2"


def usage():
    print "Usage: python {0} <event_details>\n" \
          "Example: python {0} ./events/SantaBarbaraWoB_EventDetails.txt".format(sys.argv[0])


# Chooses between SingleVenue & TwoVenues template based on number of venues defined in the event
def find_template_filenames(_event_details_props):
    if SECOND_VENUE_PROPERTY_NAME in _event_details_props:
        return TWO_VENUES_TEMPLATE_FILENAMES
    else:
        return SINGLE_VENUE_TEMPLATE_FILENAMES


# From the template filename like: templates/TeacherLedIE_WoB_VolCredit_SingleVenue_Template.xml
# creates the output file as: generated-forms/santabarbara/TeacherLedIE_WoB_VolCredit_SingleVenue_SantaBarbara.xml
def generate_form_filename(_template_filename, _event_details_props):
    city = _event_details_props[CITY_PROPERTY_NAME].replace(" ", "")
    lowercase_city = city.lower()
    return _template_filename.replace(TEMPLATES_FOLDER, GENERATED_FORMS_FOLDER + "/" + lowercase_city) \
        .replace("Template", city)


if len(sys.argv) != 2:
    usage()
    exit()

event_details_filename = sys.argv[1]
with open(event_details_filename, 'r') as event_details_file:
    event_details = event_details_file.read()

event_details_props = {}
for prop in event_details.split('\n'):
    if len(prop) == 0:
        continue
    tokens = prop.split('=')
    event_details_props[tokens[0].strip()] = tokens[1].strip()

# Uncomment to debug
# print "Using event details: " + event_details_props

template_filenames = find_template_filenames(event_details_props)

for template_filename in template_filenames:
    with open(template_filename, 'r') as template_file:
        template_content = Template(template_file.read())

    # Allow for recursive references to place holders
    previous_content = template_content
    while True:
        after_substitution = previous_content.safe_substitute(event_details_props)
        if previous_content.template == after_substitution:
            break
        previous_content = Template(after_substitution)

    output_filename = generate_form_filename(template_filename, event_details_props)

    if not os.path.exists(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))

    with open(output_filename, "w") as form_file:
        form_file.write(after_substitution)
