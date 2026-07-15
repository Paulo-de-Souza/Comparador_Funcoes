from dataclasses import dataclass, field


@dataclass
class FunctionInfo:
    name: str
    lineno: int
    end_lineno: int
    nlines: int
    source: str

    calls: list[str] = field(default_factory=list)

    variables: list[str] = field(default_factory=list)
    local_variables: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


@dataclass
class FileInfo:
    filename: str

    imports: list[str] = field(default_factory=list)

    functions: list[FunctionInfo] = field(default_factory=list)