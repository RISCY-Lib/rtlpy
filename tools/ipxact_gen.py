from __future__ import annotations

import pathlib
import textwrap
import xml.etree.ElementTree as ET

import subprocess


def main() -> None:
    create_common_module()


def create_common_module() -> None:
    body = create_module_body(pathlib.Path(__file__).parent / "1685-2022" / "autoConfigure.xsd")
    body += create_module_body(pathlib.Path(__file__).parent / "1685-2022" / "simpleTypes.xsd")
    body += ["\n"]

    fixed_body = []
    for line in body:
        if "import" in line:
            fixed_body.insert(0, line)
        else:
            fixed_body.append(line)

    with open("common.py", "w") as module_file:
        module_file.write("\n".join(fixed_body))

    subprocess.run(["uv", "run", "ruff", "check", "--fix", "--preview", "common.py"], check=True)


def create_module_body(schema_path: pathlib.Path) -> list[str]:
    body: list[str] = []

    schema = ET.parse(schema_path).getroot()
    for component in schema:
        if "simpleType" in component.tag:
            body.extend(create_simple_type(component))

    return body


def create_simple_type(component: ET.Element) -> list[str]:
    body: list[str] = []
    if (restriction := component.find("{http://www.w3.org/2001/XMLSchema}restriction")) is not None:
        if restriction.find("{http://www.w3.org/2001/XMLSchema}enumeration") is not None:
            print("Found enumeration")
            body.extend(create_enumeration(component))
        else:
            print("Found other restriction")

    return body


def create_enumeration(component: ET.Element) -> list[str]:
    body: list[str] = []
    body.append("import enum")

    body.append(f"class {str(component.attrib['name']).capitalize()}(enum.Enum):")
    if (annotation := component.find("{http://www.w3.org/2001/XMLSchema}annotation")) is not None:
        if (documentation := annotation.find("{http://www.w3.org/2001/XMLSchema}documentation")) is not None:
            docstring = textwrap.wrap(str(documentation.text).strip(), width=70)
            body.append(f"    \"\"\"{docstring[0]}")
            if len(docstring) > 1:
                for line in docstring[1:]:
                    body.append(f"    {line}")
            body.append("    \"\"\"")

    restriction = component.find("{http://www.w3.org/2001/XMLSchema}restriction")
    if restriction is None:
        raise ValueError("Expected restriction in simpleType")

    for enumeration in restriction.findall("{http://www.w3.org/2001/XMLSchema}enumeration"):
        value = enumeration.get("value")
        if value:
            body.append(f"    {value.upper()} = '{value}'")
    return body


if __name__ == "__main__":
    main()
