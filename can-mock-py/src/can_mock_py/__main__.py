import argparse

from can_mock_py.sender import (
    DEFAULT_BITRATE,
    DEFAULT_CHANNEL,
    DEFAULT_INTERVAL,
    MockCanSender,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="slcan 経由で擬似マシンの CAN フレームを送信する (can-mock の Python 版)",
    )
    parser.add_argument(
        "-c",
        "--channel",
        default=DEFAULT_CHANNEL,
        help=f"slcan アダプタのシリアルポート (default: {DEFAULT_CHANNEL})",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        type=int,
        default=DEFAULT_BITRATE,
        help=f"CAN ビットレート [bps] (default: {DEFAULT_BITRATE})",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=DEFAULT_INTERVAL,
        help=f"送信間隔 [s] (default: {DEFAULT_INTERVAL})",
    )
    args = parser.parse_args()

    sender = MockCanSender(
        channel=args.channel,
        bitrate=args.bitrate,
        interval=args.interval,
    )
    print(
        f"slcan {args.channel} @ {args.bitrate}bps で送信開始 "
        f"(間隔 {args.interval}s)。Ctrl-C で停止。"
    )
    try:
        sender.sendEvery()
    except KeyboardInterrupt:
        print("\n停止します。")
    finally:
        sender.close()


if __name__ == "__main__":
    main()
