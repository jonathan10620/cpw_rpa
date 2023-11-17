import PySimpleGUI as sg
from datetime import datetime
from dateutil.relativedelta import relativedelta



def get_year_dos(date):
    input_date = datetime.strptime(date, '%m/%d/%Y')

    new_date = input_date + relativedelta(years=1) - relativedelta(days=1)
    new_date_string = new_date.strftime('%m/%d/%Y')

    return f'{date}-{new_date_string}'

# portal id, fax
top_frame = [
    [sg.Text("Portal:"), sg.Push(), sg.InputText(key="portal_id", size=(10))],
    [
        sg.Text("Fax:"),
        sg.Push(),
        sg.InputText(key="fax_number", size=(10)),
    ],
]


mid_frame = [
    [sg.Text("MCO", key="MCO_TEXT"), sg.Push(), sg.Checkbox("", key="MCO")],
    [
        sg.Text("Start date:", key="mco_text"),
        sg.Push(),
        sg.InputText(key="mco_start_date", visible=False, size=(10)),
    ],
    [
        sg.Text("Intake Date:"),
        sg.Push(),
        sg.InputText(key="intake_date", size=(10)),
    ],
    [sg.Text("Age"), sg.Push(), sg.InputText(key="age", size=(3))],
    [
        sg.Radio("Child", "demographic", key="demographic", default=True),
        sg.Radio("Pregnant Woman", "demographic"),
    ],
    [sg.Text("Condition")],
    [sg.Multiline(default_text="", key="condition", size=(30, 4))],
]

bottom_frame = [
    [
        sg.Button("Copy"),
    ]
]



layout = [
    [sg.Frame("top", top_frame, expand_x=True)],
    [sg.Frame("middle", mid_frame, expand_x=True)],
    [sg.Frame("bottom", bottom_frame, expand_x=True)],
]

window = sg.Window("CPW", layout)


def generate_blurb(pid, fax, mco, intake_date, age, demographic, condition):
    if demographic:
        demographic = "child age (0-20)"
    else:
        demographic = "pregnant woman"
    if mco:
        return f"Portal ID: {pid} Fax #: {fax}. Please note: The client/member will be enrolled in an MCO effective {mco}. Please contact the client/member's managed cared organization for authorization requirements and authorizations. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 07. No current or future PDC. Submitted certification page submitted and completed. Date intake completed: {intake_date}. Client age: {age}y. Client is a {demographic} with a high risk condition: {condition} which results in limitation in function. DOS {get_year_dos(intake_date)} are approved based on Texas Medicaid Medical Policy Manual- {datetime.now().strftime('%B')} 2023 CPW Services. J. Delapaz RN"
    else:
        return f"Portal ID: {pid} Fax #: {fax}. Client is eligible. Duplicates/history checked. None found. Provider is eligible. Provider type: 07. No current or future PDC. Submitted certification page submitted and completed. Date intake completed: {intake_date}. Client age: {age}y. Client is a {demographic} with a high risk condition: {condition} which results in limitation in function. DOS {get_year_dos(intake_date)} are approved based on Texas Medicaid Medical Policy Manual- {datetime.now().strftime('%B')} 2023 CPW Services. J. Delapaz RN"


while True:
    event, values = window.read(timeout=150)

    pid = values["portal_id"]
    fax = values["fax_number"]
    mco = values["mco_start_date"]
    intake_date = values["intake_date"]
    age = values["age"]
    demographic = values["demographic"]
    condition = values["condition"]

    if values["MCO"]:
        window["mco_text"].update(visible=True)
        window["mco_start_date"].update(visible=True)

    else:
        window["mco_text"].update(visible=False)
        window["mco_start_date"].update(visible=False)
        window["mco_start_date"].update(value="")

    if event == "Copy":
        print(generate_blurb(pid, fax, mco, intake_date, age, demographic, condition))


window.close()
