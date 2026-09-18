import openai

import config
from services.schema import FactSheet

SYSTEM_PROMPT = """You are drafting a professional "fact sheet" for a school Principal. The \
Principal may forward this document to their own supervisor (e.g. a system or regional \
education office) or use it for external marketing, so it must be accurate and defensible \
enough that no reasonable supervisor would object to it.

You will be given (1) the text of a government education policy, and (2) a description of an \
education program called EMP. Your job is to explain how EMP is consistent with and supports \
that specific policy.

Follow these rules strictly:

1. Ground every claim about EMP only in the supplied EMP description. Never invent features, \
statistics, endorsements, partners, or claims that are not present in that text. You may \
rephrase, summarise, or select whichever supplied facts are most relevant to this policy, but \
never add new ones.
2. Ground every claim about the policy only in the supplied policy text. Never fabricate \
quotes, section numbers, or requirements. If the supplied text is incomplete or ambiguous, \
stay general rather than inventing specifics.
3. Write in a formal, neutral, evidence-led register appropriate for a Principal to forward to \
a supervisor. Do not use superlatives ("best", "guaranteed", "proven to outperform"), do not \
promise specific outcomes for any individual school, and do not imply that the policy issuer \
endorses or has reviewed EMP.
4. Phrase any outcomes/evidence about EMP as EMP's own self-reported results (e.g. "EMP \
reports..."), never as independently verified research or as a general truth.
5. Produce 4 to 6 alignment points, each tying one specific policy requirement to one specific \
EMP feature, with a short explanation of the connection.

Do not include a disclaimer or footer section — that is handled separately."""


class GenerationError(Exception):
    pass


def generate_fact_sheet(policy_text: str, emp_description: str, jurisdiction_or_policy_name: str, truncated: bool) -> FactSheet:
    if not config.OPENAI_API_KEY:
        raise GenerationError(
            "OPENAI_API_KEY is not configured. Add it to a .env file in the project root and restart."
        )

    user_parts = []
    if jurisdiction_or_policy_name:
        user_parts.append(f"Jurisdiction / policy name (as provided by the user): {jurisdiction_or_policy_name}")
    if truncated:
        user_parts.append(
            "Note: the policy text below was truncated to fit; treat it as a partial excerpt "
            "and stay general where detail is missing."
        )
    user_parts.append("=== POLICY TEXT ===\n" + policy_text)
    user_parts.append("=== EMP DESCRIPTION ===\n" + emp_description)

    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

    try:
        response = client.responses.parse(
            model=config.OPENAI_MODEL,
            instructions=SYSTEM_PROMPT,
            input="\n\n".join(user_parts),
            text_format=FactSheet,
            max_output_tokens=4000,
        )
    except openai.AuthenticationError:
        raise GenerationError("The OpenAI API rejected the configured API key. Check OPENAI_API_KEY in .env.")
    except openai.RateLimitError:
        raise GenerationError("The OpenAI API is rate-limiting requests right now. Please wait a moment and try again.")
    except openai.APIConnectionError:
        raise GenerationError("Could not reach the OpenAI API. Check your internet connection and try again.")
    except openai.APIStatusError as exc:
        raise GenerationError(f"The OpenAI API returned an error (status {exc.status_code}). Please try again.")

    parsed = response.output_parsed
    if parsed is None:
        raise GenerationError("Unexpected response from the AI model; please try again.")
    return parsed
