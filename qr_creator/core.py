import argparse
import sys
import os
import qrcode
major = "1"
minor = "1"
micro = "0"

__version__ = ".".join([major, minor, micro])

DESCRIPTION = """Encode a data into a qr code. By default reads from STDIN and writes to STDOUT
but these can be changed with -os and -of and -ins -inf
"""


def get_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--fore-color", "-fc",
                        help="Which color to use as the foreground color, defaults to 'black'",
                        default="black",
                        )
    parser.add_argument("--back-color", "-bc",
                        help="Which color to use as the background color, defaults to 'white'",
                        default="white",
                        )

    parser.add_argument("--border", "-b",
                        help="Increase or decrease the thickness of border, defaults to '4' and cannot be lower then",
                        default=4, type=int,
                        )

    parser.add_argument("--input-file", "-inf",
                        help="Which file to get data from, Overrides sooner -ins",
                        default="-", dest="input",
                        )
    parser.add_argument("--input-stream", "-ins",
                        help="File descriptor to use as input, overrides sooner -inf",
                        default=sys.stdin.fileno(), dest="input", type=int,
                        )
    parser.add_argument("--size", "-s",
                        help="Increase the size, defaults to whatever suits your data, the biggest is 40",
                        default=None, type=int,
                        )
    parser.add_argument("--output-file", "-of",
                        help="Which file to store output as",
                        dest="output",
                        )
    parser.add_argument("--output-stream", "-os",
                        help="File descriptor to use as output, overrides sooner -of",
                        default=sys.stdout.fileno(), dest="output", type=int,
                        )
    parser.add_argument("--kind", "-k",
                        help="What kind of picture do you want, defaults to 'png'",
                        default="png",
                        )
    parser.add_argument("--png",
                        help="Same as --kind=png", action="store_const",
                        const="png", dest="kind")
    parser.add_argument("--jpeg",
                        help="Same as --kind=jpeg", action="store_const",
                        const="jpeg", dest="kind")
    parser.add_argument("--ico",
                        help="Same as --kind=ico", action="store_const",
                        const="ico", dest="kind")
    parser.add_argument("--bmp",
                        help="Same as --kind=bmp",
                        const="bmp", dest="kind", action="store_const",)
    parser.add_argument("--no-logo",
                        help="Suppress the banner",
                        default=False, action="store_true",
                        )
    parser.add_argument("--log-level",
                        help="Set debug level",
                        default="WARNING")
    parser.add_argument("--verbose",
                        help="Same as --log-level DEBUG",
                        const="DEBUG", dest="log_level", action="store_const")
    parser.add_argument("--quiet",
                        help="Same as --log-level CRITICAL",
                        const="CRITICAL", dest="log_level", action="store_const")
    return parser


def print_banner(dont=False):
    if not dont:
        print(f"QR-Creator v{__version__}, Easily create QR codes")
        print("Written by TheOddZer0 See COPYING file for more info")
        print("See original repo for updates, more info: https://github.com/TheOddZer0/QR-Creator")
        print("")


def get_input():
    data = b""
    while True:
        z = b""
        try:
            z = sys.stdin.buffer.read()
            if z == b"":
                return data
            data += z
        except KeyboardInterrupt:
            print()
            return None


def handle_args(ns, logger):
    logger.debug("Making sure arguments are all in-order")
    found = 0
    if ns.border < 4:
        found = 1
        logger.warning("'Boarder' cannot be lower then 4, going with 4")
        ns.border = 4
    if ns.size is not None and 0 > ns.size > 40:
        logger.warning(
            "Invalid size, going with the most suitable for the data")
        ns.size = None
        found = 1
    if found:
        logger.debug("Found a mismatch which is ignored")
    else:
        logger.debug("Everything is in-order")


def get_data(filename, logger):
    logger.debug(f"Handling a file with the name '{filename}'")
    if filename not in ("-", sys.stdin.fileno()):
        try:
            if isinstance(filename, int):
                f = os.fdopen(filename, "rb")
            else:
                f = open(filename, "rb")
            data = f.read()
            return data
        except OSError:
            logger.critical("Could not open file/stream, Exiting...", exc_info=1)
            raise SystemExit(1) from None
        

    else:
        logger.debug(f"File is `{filename}`, Reading from STDIN")
        data = get_input()
        if data is None:
            logger.warning("get_input got KeyboardInterrupt, Exiting...")
            raise SystemExit(1) from None
        logger.debug("Done reading from STDIN")
        return data


def init_factory(ns, data, logger):
    logger.debug("Initializing the factory")
    try:
        qr = qrcode.QRCode(version=ns.size, border=ns.border)
        logger.debug("Done, Feeding it with enough data")
        qr.add_data(data)
        qr.make()
        factory = qr.make_image(fill_color=ns.fore_color,
                                back_color=ns.back_color)
        factory.kind = ns.kind
    except Exception:
        logger.critical("Could not get the factory working", exc_info=1)
        raise SystemExit(1) from None
    return factory


def save_image(factory, ns, logger):
    if not ns.kind.startswith("."):
        ns.kind = "." + ns.kind
    logger.debug(f"Saving QR code data to '{ns.output + ns.kind}'")
    try:
        if isinstance(ns.output, int):
            f = os.fdopen(ns.output, "wb")
        else:
            f = open(ns.output + ns.kind, "wb")
    except OSError:
        logger.critical("Could not open output to write, Got: ", exc_info=1)
        raise SystemExit(1) from None
    try:
        factory.save(f)
        logger.debug("Done, QR Saved")
    except KeyError:
        logger.warn("'{ns.kind}' is not recognized, Falling back on fake-png")
        factory.save(f, format = "png")
        logger.debug("Done, QR Saved (fake-png)")
    