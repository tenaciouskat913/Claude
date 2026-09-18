from datetime import date

import streamlit as st

import config
from services.llm_client import GenerationError, generate_fact_sheet
from services.docx_builder import build_docx, slugify
from services.url_extractor import ExtractionError, fetch_policy_text


st.set_page_config(
    page_title="EMP Policy Fact Sheet Generator",
    page_icon="📄",
    layout="wide",
)

st.title("EMP Policy Fact Sheet Generator")

st.write(
    "Generate an EMP fact sheet from a policy webpage or pasted policy text."
)

# --------------------------------------------------
# EMP DESCRIPTION
# --------------------------------------------------

emp_description = st.text_area(
    "EMP description",
    value=config.DEFAULT_EMP_DESCRIPTION,
    height=180,
)

# --------------------------------------------------
# POLICY DETAILS
# --------------------------------------------------

jurisdiction_or_policy_name = st.text_input(
    "Jurisdiction or policy name",
    placeholder="e.g. ACT Strong Foundations",
)

mode = st.radio(
    "How would you like to provide the policy?",
    ["Policy URL", "Paste policy text"],
)

policy_text = ""

if mode == "Policy URL":
    policy_url = st.text_input(
        "Policy URL",
        placeholder="https://...",
    )
else:
    policy_text = st.text_area(
        "Policy text",
        height=300,
        placeholder="Paste the policy text here...",
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

if st.button("Generate fact sheet", type="primary"):

    if not emp_description.strip():
        st.error("EMP description cannot be empty.")
        st.stop()

    try:

        if mode == "Policy URL":

            if not policy_url.strip():
                st.error("Please provide a policy URL.")
                st.stop()

            with st.spinner("Reading policy webpage..."):
                policy_text = fetch_policy_text(policy_url.strip())

        else:

            policy_text = policy_text.strip()

            if not policy_text:
                st.error("Please paste the policy text.")
                st.stop()

    except ExtractionError as exc:
        st.error(str(exc))
        st.stop()

    # Limit policy length
    truncated = len(policy_text) > config.MAX_POLICY_TEXT_CHARS

    if truncated:
        policy_text = policy_text[:config.MAX_POLICY_TEXT_CHARS]
        st.warning(
            "The policy text was very long and has been shortened "
            "before being sent for analysis."
        )

    # Generate fact sheet
    try:

        with st.spinner("Generating EMP fact sheet..."):

            factsheet = generate_fact_sheet(
                policy_text=policy_text,
                emp_description=emp_description.strip(),
                jurisdiction_or_policy_name=
                    jurisdiction_or_policy_name.strip(),
                truncated=truncated,
            )

    except GenerationError as exc:
        st.error(str(exc))
        st.stop()

    # Save result so it survives Streamlit reruns
    st.session_state["factsheet"] = factsheet.model_dump()


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

if "factsheet" in st.session_state:

    factsheet = st.session_state["factsheet"]

    st.divider()

    st.header(factsheet.get("title", "EMP Fact Sheet"))

    # Show generated data
    st.json(factsheet)

    # --------------------------------------------------
    # CREATE WORD DOCUMENT
    # --------------------------------------------------

    try:

        buffer = build_docx(factsheet)

        # Make sure we're at the beginning of the buffer
        buffer.seek(0)

        filename = (
            f"EMP_FactSheet_"
            f"{slugify(factsheet.get('title', ''))}_"
            f"{date.today().isoformat()}.docx"
        )

        st.download_button(
            label="Download Word document",
            data=buffer.getvalue(),
            file_name=filename,
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
        )

    except Exception as exc:
        st.error(f"Could not create the Word document: {exc}")