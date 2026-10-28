# Lab 5 reflection

The supplied handout requests reflection answers but does not list the questions.
These four responses address its stated learning outcomes.

## 1. What did each tool contribute?

Pylint exposed the shared default audit list, swallowed exceptions, unused values,
resource handling and naming problems. Flake8 identified formatting problems.
Bandit's role is to identify security-sensitive patterns such as shell execution,
dynamic evaluation, weak hashes, embedded credentials and insecure randomness.
These scopes overlap, but one tool cannot replace the other two.

## 2. Which problems were most important to fix?

The shell call and `eval` accepted data that could become executable instructions.
Removing those execution paths was more important than changing formatting.
The hardcoded token also needed removal from both source and output. Replacing
MD5 and the OTP random generator addressed inappropriate security primitives.

## 3. How were the fixes checked?

Before reports preserve the original Pylint and Flake8 findings. The cleaned
source reaches 10.00/10 in Pylint and produces no Flake8 findings. Regression
tests verify enrollment behavior and security boundaries instead of checking
style alone. Bandit verification is completed by the report-generation command
once its dependency is installed; a missing tool must not be reported as a pass.

## 4. What are the limitations and lessons?

Static tools identify suspicious patterns, not the full business specification.
They cannot establish whether a student really enrolled before a drop or whether
a tuition refund is correct without a richer domain model. Manual review found
import-time execution and inconsistent seat availability. Future work should
combine static checks, unit tests and explicit domain requirements. A high
lint score is useful evidence of code quality, not proof of correctness.
