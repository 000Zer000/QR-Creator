from qr_creator import logger as _logger, core


def _real_main(ns):
    core.print_banner(ns.no_logo)
    logger = _logger.get_logger(ns)
    try:
        import QRCreator
        del QRCreator
        logger.warning("The old QRCreator is still installed, Use pip uninstall QRCreator")
    except ImportError:
        pass
    core.handle_args(ns, logger)
    logger.info(ns)  # This may come in handy
    try:
        data = core.get_data(ns.input, logger)
    except BaseException as e:
        if isinstance(e, SystemExit):
            raise
        logger.critical("get_data failed with exception: ", exc_info=1)
        raise SystemExit(1) from None
    factory = core.init_factory(ns, data, logger)


def main():
    try:
        _real_main(core.get_parser().parse_args())
    except KeyboardInterrupt:
        print("qr-creator: User requested exit, exiting...")
    


if __name__ == '__main__':
    main()
