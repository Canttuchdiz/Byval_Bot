from discord import Embed, Color
from re import compile
from enum import Enum


class _Lang(Enum):
    awk = "awk"
    bash = "bash"
    befunge93 = "befunge93"
    brachylog = "brachylog"
    brainfuck = "bf"
    bqn = "bqn"
    c = "c"
    cjam = "cjam"
    clojure = "clojure"
    cobol = "cobol"
    coffeescript = "coffeescript"
    cow = "cow"
    cpp = "cpp"
    crystal = "crystal"
    csharp = "cs"
    d = "d"
    dart = "dart"
    dash = "dash"
    dragon = "dragon"
    elixir = "elixir"
    emacs = "emacs"
    emojicode = "emojicode"
    erlang = "erlang"
    file = "file"
    forte = "forte"
    forth = "forth"
    fortran = "fortran"
    freebasic = "freebasic"
    fsi = "fsi"
    go = "go"
    golfscript = "golfscript"
    groovy = "groovy"
    haskell = "haskell"
    husk = "husk"
    iverilog = "iverilog"
    japt = "japt"
    java = "java"
    javascript = "js"
    jelly = "jelly"
    julia = "julia"
    kotlin = "kotlin"
    lisp = "lisp"
    llvm_ir = "llvm_ir"
    lolcode = "lolcode"
    lua = "lua"
    matl = "matl"
    nasm = "nasm"
    nasm64 = "nasm64"
    nim = "nim"
    ocaml = "ocaml"
    octave = "octave"
    osabie = "osabie"
    paradoc = "paradoc"
    pascal = "pascal"
    perl = "perl"
    php = "php"
    ponylang = "ponylang"
    powershell = "powershell"
    prolog = "prolog"
    pure = "pure"
    pyth = "pyth"
    python = "py"
    python2 = "python2"
    racket = "racket"
    raku = "raku"
    retina = "retina"
    rockstar = "rockstar"
    rscript = "rscript"
    ruby = "ruby"
    rust = "rust"
    samarium = "samarium"
    scala = "scala"
    smalltalk = "smalltalk"
    sqlite3 = "sqlite3"
    swift = "swift"
    typescript = "ts"
    basic = "basic"
    vlang = "vlang"
    vyxal = "vyxal"
    yeethon = "yeethon"
    zig = "zig"


class _Embeds:
    embms = "{0} Runtime"
    embnl = "Invalid Language: {0}"
    embs = {True: Embed(title="Execution Completed", color=Color.green()),
            False: Embed(title="Execution Error", color=Color.red()),
            str: Embed(title="Compilation Error", color=Color.red())}


class _RegexExp:
    ROLE_MENTION = compile(r"\<@&\d{18,}\>")


class _DiscordLimits:
    FIELD_MAX = 1024
