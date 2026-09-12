from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"

CORPUS.mkdir(exist_ok=True)


# ============================================================
# MAIN RULEBOOK SECTIONS
# ============================================================

sections = {

    "1. Academic Calendar and Registration": """
    The academic year is divided into two regular semesters, an autumn semester and a spring semester.
    Students must complete online registration before the registration deadline published by the Academic Office.
    Registration requires confirmation of the student's program, semester, registered courses, and fee status.

    A student who does not complete registration by the announced deadline may be prevented from attending
    classes until registration is regularized. Students should verify their registered courses before the
    course-add deadline. Changes after the course-add period require approval from the Academic Office.

    Students are responsible for checking official notices published through the university student portal.
    Failure to read a notice does not normally exempt a student from an announced academic deadline.

    Students entering a new academic year must satisfy progression requirements applicable to their program.
    Students with academic deficiencies should consult their department before registering for courses.

    The Academic Office maintains the official academic calendar. Department-level announcements may provide
    additional operational information, but they cannot automatically replace university-wide deadlines.
    """,

    "2. Course Registration and Add/Drop": """
    Students may register for courses offered in their program subject to prerequisites, seat availability,
    and academic restrictions. A prerequisite course must normally be completed before enrolling in the
    course that requires it.

    During the add/drop period, students may add an eligible course or withdraw from a course according
    to the procedure announced by the Academic Office. A dropped course during the permitted period will
    not normally appear as a completed course on the academic transcript.

    After the add/drop period, course changes require authorization. Students should not assume that
    informal permission from a class representative or instructor is sufficient.

    Students should review their timetable after every approved registration change. Timetable conflicts
    must be reported promptly. The university may refuse a registration request if attendance or
    assessment requirements cannot reasonably be fulfilled.

    Students are responsible for understanding the workload associated with every registered course.
    Registration in a course indicates that the student accepts its assessment requirements.
    """,

    "3. Attendance Requirements": """
    Students are expected to attend all scheduled instructional activities. Regular attendance is an
    essential academic requirement because classroom participation, laboratory activities, tutorials,
    and practical demonstrations may form part of a course.

    The minimum attendance requirement for eligibility for the final examination is 75 percent in each
    registered course. Attendance is calculated using the instructional sessions recorded by the
    department.

    Students should maintain their own attendance records and report discrepancies to the course
    instructor within the period announced by the department. A discrepancy reported after records have
    been finalized may not be considered.

    Attendance cannot normally be substituted by submitting additional assignments unless the relevant
    course policy expressly permits such substitution.

    Students who are repeatedly absent may receive an academic warning. The department may ask a student
    to meet an academic advisor when attendance falls substantially below the expected level.

    For laboratory courses, attendance may be separately important because practical work cannot always
    be recreated outside the scheduled laboratory session.

    The minimum attendance requirement stated in this section is 75 percent and applies to all students.
    """,

    "4. Medical Absence and Exceptional Attendance": """
    A student experiencing a documented medical condition may submit supporting medical documentation to
    the designated academic office. The documentation should identify the period during which the student
    was medically unable to participate in academic activities.

    For an approved medical absence, the department may record the absence as medically authorized.
    Students should submit the documentation as soon as reasonably possible after returning to academic
    activities.

    An approved medical absence does not automatically cancel every academic requirement. The student
    may still be required to complete missed laboratory work, assessments, presentations, or other
    course-specific requirements.

    The department may consider an approved medical absence when reviewing attendance eligibility.
    Students should obtain written confirmation of the decision rather than relying on verbal assurances.

    The medical attendance provision is intended for genuine documented circumstances and should not be
    used as a general mechanism for avoiding regular attendance.
    """,

    "5. Examination Eligibility": """
    Students must satisfy course requirements before appearing in the final examination. These requirements
    may include attendance, registration status, internal assessment completion, and payment of applicable
    academic fees.

    A student who does not meet the minimum attendance requirement may be declared ineligible for the
    final examination. The department publishes the list of students whose examination eligibility has
    been restricted.

    The examination eligibility process is intended to ensure that students participate sufficiently
    in instructional activities before being assessed.

    Students who believe an eligibility decision contains an administrative error may submit an appeal
    within the period announced by the Academic Office.

    Under the general examination rule, no student below 75 percent attendance may sit for the final
    examination under any circumstances.
    """,

    "6. Internal Assessment": """
    Internal assessment may consist of quizzes, assignments, laboratory work, presentations, projects,
    mid-semester examinations, or other activities defined in the course outline.

    Students should monitor assessment announcements issued by the instructor. An assessment submitted
    after its deadline may receive a penalty where the course policy permits such a penalty.

    Instructors should communicate major assessment requirements in advance. Students are expected
    to retain evidence of submissions where the submission system provides a receipt.

    Academic work submitted by a student must represent the student's own work except where collaboration
    is explicitly permitted. Group assignments must identify participating students according to the
    instructions provided by the instructor.

    Internal assessment records should be reviewed before final grades are published.
    """,

    "7. Final Examinations": """
    Final examinations are conducted according to the examination schedule issued by the university.
    Students must verify the date, time, venue, and examination instructions before appearing.

    Students should carry the identification document permitted by the examination authority. Unauthorized
    materials, electronic devices, or communication with other candidates may constitute examination
    misconduct.

    Students should arrive before the reporting time. Entry after the permitted late-entry period may
    be restricted.

    The examination authority may change a venue or schedule when operational circumstances require it.
    Students are responsible for checking official announcements before an examination.

    Students should follow instructions provided by invigilators. Disputes during an examination should
    normally be reported through the formal examination grievance procedure rather than disrupting the
    examination.
    """,

    "8. Examination Conduct": """
    Examination conduct requires honesty, independence, and compliance with invigilation instructions.
    Copying, unauthorized communication, possession of prohibited material, impersonation, or deliberate
    interference with examination procedures may be treated as academic misconduct.

    If an invigilator suspects misconduct, the incident may be documented and referred to the appropriate
    disciplinary authority.

    A student should not remove examination material from the examination hall unless explicitly permitted.

    Electronic devices must remain in the condition specified by the examination instructions. A device
    that is not permitted may be treated as unauthorized material even if the student claims that it was
    not actively used.

    Students should raise questions about examination instructions before beginning whenever possible.
    """,

    "9. Grading and Grade Review": """
    Course grades are determined using the assessment structure specified for the course. The relative
    weight of internal assessment, practical work, projects, and final examinations should be available
    through the course documentation.

    Students may request clarification of a published grade through the designated procedure. A request
    for review should identify the course, assessment, and specific concern.

    A grade review does not guarantee an increase. The review may confirm the original result or identify
    an administrative or evaluation error.

    Students should not pressure instructors or administrative staff to alter grades outside the formal
    review process.

    The university maintains academic records according to its record-retention procedures.
    """,

    "10. Academic Integrity": """
    Academic integrity requires students to present their own academic work honestly. Plagiarism includes
    presenting another person's words, ideas, analysis, or work as one's own without appropriate
    acknowledgment.

    Fabrication of data, falsification of records, unauthorized collaboration, impersonation, and other
    forms of dishonest academic behavior may be investigated.

    Students using external sources should follow the citation requirements applicable to the assignment.
    The use of an AI-based tool does not automatically make submitted work original; students remain
    responsible for the accuracy and academic integrity of their submissions.

    Where collaboration is permitted, students should comply with the specified limits. Unauthorized
    collaboration can be treated as academic misconduct.

    Students accused of misconduct should receive information about the applicable disciplinary process.
    """,

    "11. Course Withdrawal": """
    A student may withdraw from an eligible course during the withdrawal period published in the academic
    calendar. Withdrawal after the deadline requires the approvals specified by the Academic Office.

    A withdrawal request should be submitted through the official student system or designated office.
    Informal communication with an instructor does not by itself complete the withdrawal process.

    Students should consider the effect of withdrawal on workload, prerequisites, progression, scholarships,
    and graduation requirements before submitting a request.

    The transcript treatment of an approved withdrawal follows the academic-record rules applicable to
    the student's program.
    """,

    "12. Scholarships and Financial Support": """
    Scholarships and financial assistance are subject to their individual eligibility conditions. Students
    should review the published requirements for academic performance, enrollment status, documentation,
    and application deadlines.

    Receiving financial support in one semester does not automatically guarantee support in later semesters.
    Students may be required to submit updated documentation.

    Students must notify the appropriate office if a material change affects their eligibility.

    The financial-aid office may request supporting documents and may reject incomplete applications.
    """,

    "13. Student Identification": """
    Students must use their assigned student identification number in official academic communications.
    The identification card may be required for examinations, laboratory access, library services, and
    other university facilities.

    Students should report a lost identification card promptly. A temporary identification process may
    be available according to administrative instructions.

    Students must not lend their identification credentials to another person. Misuse of identification
    may result in administrative or disciplinary action.
    """,

    "14. Library Rules": """
    Students may borrow library materials according to the borrowing limits applicable to their category.
    Materials must be returned by the stated due date.

    Renewal may be available when an item has not been reserved by another user. Some reference materials,
    rare materials, or short-loan resources may not be renewable.

    Students are responsible for materials issued against their account. Damaged or lost materials may
    result in replacement or recovery charges according to library policy.

    Library users should maintain a quiet environment and comply with instructions from library staff.
    """,

    "15. Laboratory Safety": """
    Students participating in laboratory activities must follow safety instructions provided by the
    department and laboratory staff.

    Required protective equipment must be used where specified. Students should not operate equipment
    without appropriate authorization or supervision.

    Electrical, chemical, mechanical, and computing laboratory environments may have different safety
    requirements. Students must read the instructions applicable to the laboratory before beginning work.

    Accidents, equipment damage, and unsafe conditions should be reported promptly to laboratory staff.

    Students should not modify laboratory equipment or bypass safety mechanisms without authorization.
    """,

    "16. Project and Internship Requirements": """
    Project courses may require proposal submission, periodic reviews, documentation, demonstrations, and
    a final report. Students should follow the milestones published by the department.

    Internship activities must satisfy the requirements of the relevant academic program where internship
    credit is being claimed.

    Students are responsible for maintaining evidence of approved project or internship activities.
    Supervisors may evaluate progress according to the published criteria.

    A project submission must comply with academic-integrity requirements and should clearly identify
    external materials or contributions.
    """,

    "17. Student Grievances": """
    Students may raise academic or administrative grievances through the designated grievance mechanism.
    A grievance should state the relevant facts and identify the decision or issue being challenged.

    Students should attach supporting documents where appropriate. Anonymous allegations may not always
    provide enough information for an investigation.

    The grievance process does not automatically suspend academic deadlines. Students should request
    interim relief separately where such relief is available.

    Students should communicate respectfully with university personnel during grievance proceedings.
    """,

    "18. Disciplinary Procedure": """
    Disciplinary matters may be reviewed by the authority designated under the applicable institutional
    rules.

    A student may be informed of the allegation and given an opportunity to respond according to the
    applicable procedure.

    Possible consequences depend on the nature and seriousness of the violation and the findings of the
    competent authority.

    Students should comply with interim instructions issued during an investigation unless those
    instructions are formally changed.
    """,

    "19. Digital Systems and Cybersecurity": """
    Students using university digital systems must protect their login credentials and should not share
    passwords or authentication codes.

    Accounts may be monitored for security, operational, or compliance purposes according to institutional
    requirements.

    Students should report suspected unauthorized access or security incidents promptly.

    University computing resources should primarily be used for authorized academic, administrative, or
    other permitted purposes. Attempts to bypass security controls are prohibited.

    Students should maintain current contact information so important digital notifications can be
    delivered.
    """,

    "20. Graduation Requirements": """
    A student becomes eligible for graduation after completing the required credits, compulsory courses,
    academic requirements, and other program conditions applicable to the degree.

    Students should review their academic progress before the final semester rather than waiting until
    the graduation application period.

    Outstanding academic, financial, library, or administrative obligations may affect the completion
    process where the applicable regulations permit such restrictions.

    The graduation application must be submitted using the procedure and deadline announced by the
    Academic Office.
    """,

    "21. Academic Progression": """
    Students are expected to make satisfactory academic progress through their program.

    Progression decisions may consider earned credits, failed courses, required prerequisites, and
    program-specific requirements.

    Students with academic deficiencies should consult their academic advisor to understand their available
    options.

    A failed course must normally be completed or otherwise resolved according to the applicable academic
    rules before a student can satisfy the corresponding degree requirement.
    """,

    "22. Re-examination": """
    A student who fails an eligible course may be permitted to take a re-examination subject to the
    conditions published by the Academic Office.

    The general re-examination provision allows a maximum of two attempts to clear a failed course.
    Students should verify the examination schedule and registration procedure before attempting a
    re-examination.

    A re-examination result is recorded according to the grading rules applicable to the program.

    Students should not assume that every course is eligible for re-examination; practical or specially
    structured courses may have separate requirements.
    """,

    "23. Fee Payment": """
    Students must pay tuition and other applicable academic fees according to the deadlines announced by
    the Finance Office.

    The standard tuition fee deadline for the autumn semester is 31 August. Payments after the deadline
    may attract a late fee.

    Students should retain payment receipts or transaction references until the payment is reflected in
    their official account.

    If a payment appears unsuccessful, students should contact the Finance Office rather than making
    multiple duplicate payments without verification.

    Fee-related disputes should include the student's identification details, payment reference, amount,
    and date of transaction.
    """,

    "24. Campus Facilities": """
    Students may use campus facilities according to the rules applicable to each facility. Facility
    availability may depend on operating hours, bookings, safety restrictions, and academic requirements.

    Students should leave shared spaces in an appropriate condition and report damage to facility staff.

    Restricted areas may only be accessed by authorized persons.

    The university may temporarily close facilities for maintenance, safety, examinations, or other
    operational reasons.
    """,

    "25. Communication and Official Notices": """
    The university communicates official academic information through designated channels including the
    student portal, institutional email, and official notices.

    Students should regularly monitor these channels during the semester.

    A message shared informally through a student group should not automatically be treated as an official
    university decision unless it originates from an authorized source.

    Students should use their institutional identity when communicating with academic and administrative
    offices.
    """,
}


# ============================================================
# ADDITIONAL CONTENT
# ============================================================

extra_topics = [
    "attendance monitoring and academic advising",
    "course assessment planning",
    "student responsibilities",
    "administrative documentation",
    "academic scheduling",
    "laboratory participation",
    "examination preparation",
    "record verification",
    "department communication",
    "student portal usage",
]


for topic in extra_topics:

    sections[f"Additional Academic Guidance: {topic.title()}"] = f"""
    Students should approach {topic} in a timely and organized manner. Official academic requirements
    should always be checked before making a decision that affects registration, assessment, examination,
    progression, or graduation.

    Students are encouraged to maintain copies of important academic documents, receipts, approval
    messages, assessment submissions, and official correspondence. Keeping accurate records can make it
    easier to resolve administrative discrepancies.

    Where a procedure requires approval, students should wait for the formal approval before assuming that
    the request has been accepted. Verbal discussions can help students understand a process, but the
    official record remains the authoritative evidence of an approved request.

    Students should provide complete and accurate information in university forms. Incorrect information
    can delay processing and may require the student to submit corrected documentation.

    Academic staff and administrative offices may direct students to different procedures depending on
    the nature of a request. Students should follow the designated procedure rather than attempting to
    bypass it.

    Deadlines should be treated seriously. Students should not wait until the final hour to submit an
    important application, particularly where technical problems or incomplete documentation could prevent
    submission.

    When a student is uncertain about a rule, the safest approach is to consult the relevant official
    office and retain the response. Students should distinguish between general guidance and a formal
    approval.

    Students are expected to behave respectfully in classrooms, laboratories, examination venues,
    administrative offices, and shared campus spaces. Conduct that interferes with another student's
    academic activities may be subject to review.

    The purpose of academic regulations is to provide predictable procedures and fair treatment. Students
    should understand both their responsibilities and the available mechanisms for requesting clarification,
    review, or appeal.
    """


# ============================================================
# SUPPLEMENTARY REGULATIONS
# ============================================================

for topic in extra_topics:

    for i in range(1, 9):

        sections[
            f"Supplementary Regulation {i} - {topic.title()}"
        ] = f"""
            This supplementary regulation establishes additional administrative guidance for students.

            Students should consult official academic records before relying on information about their registration,
            attendance, assessment, examination eligibility, fees, progression, or graduation.

            A student making an academic request should provide complete information and submit the request through
            the designated institutional channel. Requests should normally include the student's identification
            number, program, semester, relevant course information, supporting documentation where applicable, and
            a clear description of the issue.

            Students are responsible for checking whether a request requires prior approval. Submission of a form
            does not necessarily mean that the request has been approved. Where an approval is required, students
            should wait for written confirmation before acting on the assumption that the request has been accepted.

            Academic records should be checked periodically. If a student identifies an error in a record, the
            student should report the discrepancy through the appropriate office and provide evidence supporting
            the requested correction.

            Students should retain copies of important notices and communications. This may include examination
            notices, registration confirmations, payment receipts, course-registration records, assessment
            submissions, approved absence documents, and formal decisions concerning academic requests.

            The university expects students to comply with published procedures even when a different procedure was
            used informally in the past. A previous administrative practice does not automatically establish a
            permanent entitlement.

            When two university communications appear inconsistent, students should not select whichever rule is
            more convenient. They should identify the relevant documents and seek clarification from the office
            responsible for the matter.

            Students should plan academic activities around published deadlines. Technical problems, network
            failures, or personal scheduling difficulties should not be assumed to extend a deadline unless the
            responsible office officially announces an extension.

            Departments may issue instructions concerning the practical operation of university-wide rules.
            Department instructions should be read together with the broader academic regulations.

            Students participating in academic activities are expected to maintain professional conduct. They
            should communicate respectfully with instructors, administrative personnel, examination staff,
            laboratory staff, library personnel, and other students.

            Academic facilities are shared resources. Students should use classrooms, laboratories, libraries,
            computing facilities, and other spaces responsibly and should follow safety and access requirements.

            Students should protect confidential academic information. They should not share another student's
            personal records, examination information, grades, credentials, or other restricted information
            without appropriate authorization.

            Digital communication should be clear and appropriate. Students should use their institutional
            accounts where required and should include sufficient information for an office to identify the
            request and respond accurately.

            Where a student is unsure about the interpretation of an academic requirement, the student should
            consult the appropriate academic authority.

            Students should review the applicable requirements before submitting important academic applications.
            Incomplete applications may require additional processing and can sometimes miss a deadline.

            The university may update procedures from time to time. Students should rely on the current official
            version of a regulation when making academic decisions.

            These supplementary provisions emphasize that students share responsibility for maintaining accurate
            records, observing deadlines, using official communication channels, and seeking clarification when
            requirements are unclear.
            """


# ============================================================
# CREATE RULEBOOK
# ============================================================

rulebook_path = CORPUS / "rulebook.md"

with open(rulebook_path, "w", encoding="utf-8") as f:

    f.write("# Model University Academic Rulebook\n\n")

    f.write(
        "> Synthetic corpus created for the Rulebook AI evaluation project. "
        "It is not an official policy of any university.\n\n"
    )

    for title, text in sections.items():

        f.write(f"## {title}\n\n")
        f.write(text.strip())
        f.write("\n\n")


print(f"Created {rulebook_path}")


# ============================================================
# CREATE FEE TABLE
# ============================================================

fee_table = """# Academic Fee Deadline Table

                    | Fee / Payment | Semester | Standard Deadline | Late Fee |
                    |---|---|---|---|
                    | Tuition Fee | Autumn | 15 September | ₹500 |
                    | Tuition Fee | Spring | 15 February | ₹500 |
                    | Examination Fee | Autumn | 10 November | ₹250 |
                    | Examination Fee | Spring | 10 April | ₹250 |
                    | Laboratory Fee | Autumn | 20 August | ₹200 |
                    | Laboratory Fee | Spring | 20 January | ₹200 |
                    | Library Renewal Charge | All Semesters | As notified | ₹100 |

                    The table above is the Finance Office's published deadline table for the purposes of this synthetic
                    evaluation corpus.
                    """

fee_path = CORPUS / "fee_table.md"

fee_path.write_text(fee_table, encoding="utf-8")

print(f"Created {fee_path}")


# ============================================================
# CREATE PDF
# ============================================================

pdf_path = CORPUS / "regulations.pdf"

styles = getSampleStyleSheet()

doc = SimpleDocTemplate(
    str(pdf_path),
    pagesize=A4
)

story = []

story.append(
    Paragraph(
        "Model University Regulations",
        styles["Title"]
    )
)

story.append(Spacer(1, 20))


pdf_sections = [

    (
        "Attendance and Examination Regulation",
        """
                            Students are normally required to maintain at least 75 percent attendance in each course
                            before appearing for the final examination. Attendance records are maintained by the relevant
                            department and students should report errors promptly.
                            """
    ),

    (
        "Medical Attendance Regulation",
        """
                            A student with an approved medical absence may be considered for examination eligibility
                            when attendance is at least 60 percent, provided the medical absence has been formally approved
                            and the required supporting documentation has been submitted.
                            """
    ),

    (
        "Course Attempts Regulation",
        """
                            A failed course may generally be cleared through a re-examination. Students are normally
                            permitted three re-examination attempts.
                            """
    ),

    (
        "Academic Records",
        """
                            Students should verify their academic records and report administrative errors through the
                            designated academic office.
                            """
    ),
]


for title, text in pdf_sections:

    story.append(
        Paragraph(
            title,
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            text,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))


# Fee table

story.append(
    Paragraph(
        "Fee Schedule",
        styles["Heading2"]
    )
)

data = [
    ["Fee", "Deadline", "Late Fee"],
    ["Tuition - Autumn", "15 September", "₹500"],
    ["Tuition - Spring", "15 February", "₹500"],
    ["Examination - Autumn", "10 November", "₹250"],
    ["Examination - Spring", "10 April", "₹250"],
]

table = Table(data)

table.setStyle(
    TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("PADDING", (0, 0), (-1, -1), 6),
    ])
)

story.append(table)

doc.build(story)

print(f"Created {pdf_path}")

# ============================================================
# CREATE CONTRADICTION DOCUMENTATION
# ============================================================

contradictions = """# Planted Contradictions

                        This file documents the three intentional contradictions in the synthetic corpus.

                        ## Contradiction 1 — Attendance / Medical Exception

                        **Location A:** `rulebook.md` → Section 3: Attendance Requirements

                        > The minimum attendance requirement stated in this section is 75 percent and applies to all students.

                        **Location B:** `regulations.pdf` → Page 1 → Medical Attendance Regulation

                        > A student with an approved medical absence may be considered for examination eligibility when attendance is at least 60 percent.

                        **Conflict:** The general rule says 75% applies to all students, while the PDF explicitly permits consideration at 60% for approved medical absence.

                        ---

                        ## Contradiction 2 — Tuition Fee Deadline

                        **Location A:** `rulebook.md` → Section 23: Fee Payment

                        > The standard tuition fee deadline for the autumn semester is 31 August.

                        **Location B:** `fee_table.md` → Academic Fee Deadline Table

                        > Tuition Fee | Autumn | 15 September | ₹500

                        **Conflict:** Two different standard autumn tuition deadlines are stated: 31 August and 15 September.

                        ---

                        ## Contradiction 3 — Re-examination Attempts

                        **Location A:** `rulebook.md` → Section 22: Re-examination

                        > The general re-examination provision allows a maximum of two attempts to clear a failed course.

                        **Location B:** `regulations.pdf` → Course Attempts Regulation

                        > A failed course may generally be cleared through a re-examination. Students are normally permitted three re-examination attempts.

                        **Conflict:** The rulebook allows a maximum of two attempts, while the PDF allows three attempts.
                        """

contradictions_path = ROOT / "contradictions.md"

contradictions_path.write_text(
    contradictions,
    encoding="utf-8"
)

print(f"Created {contradictions_path}")

# ============================================================
# FINAL STATUS
# ============================================================

print("\nCorpus generation complete.")

print(f"\nRulebook sections: {len(sections)}")

word_count = len(
    rulebook_path.read_text(encoding="utf-8").split()
)

print(f"Rulebook word count: {word_count}")

print("\nFiles created:")
print(" - corpus/rulebook.md")
print(" - corpus/fee_table.md")
print(" - corpus/regulations.pdf")
print(" - contradictions.md")
