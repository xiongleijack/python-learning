"""
05 - 面向对象

Java class / record     Python class / @dataclass
interface               鸭子类型（先会用 class 即可）
@Override               同名方法即 override（无注解）
private field           约定 _name 表示「内部使用」
"""


from dataclasses import dataclass


class ToolService:
    """类似一个简单的 Spring Service"""

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    def build_command(self, name: str) -> str:
        return f"{self._prefix}:{name}"


@dataclass
class AiConfig:
    """类似 Java record / Lombok @Data"""
    provider: str
    model: str
    max_tokens: int = 4096


class AdminToolService(ToolService):
    def build_command(self, name: str) -> str:
        return super().build_command(name).upper()


if __name__ == "__main__":
    svc = ToolService("tool")
    print(svc.build_command("git"))

    cfg = AiConfig(provider="anthropic", model="claude-opus-4-6")
    print(cfg)

    admin = AdminToolService("admin")
    print(admin.build_command("audit"))
