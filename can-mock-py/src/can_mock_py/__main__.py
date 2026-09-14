import argparse

from can_mock_py.sender import (
    DEFAULT_BITRATE,
    DEFAULT_CHANNEL,
    DEFAULT_INTERVAL,
    DEFAULT_REINIT_INTERVAL,
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
    parser.add_argument(
        "--reinit-interval",
        type=float,
        default=DEFAULT_REINIT_INTERVAL,
        help="この秒間隔で slcan チャネルを C/O 再初期化し bus-off から自動復帰する "
        f"(default: {DEFAULT_REINIT_INTERVAL}s、<=0 で無効)。ボードとの IP 到達性に依存せず "
        "CANable 単体で動く",
    )
    args = parser.parse_args()

    sender = MockCanSender(
        channel=args.channel,
        bitrate=args.bitrate,
        interval=args.interval,
        reinit_interval=args.reinit_interval,
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
