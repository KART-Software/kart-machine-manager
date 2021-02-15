import QtQuick 2.13
import QtQuick.Window 2.13
import QtQuick.Controls 2.5
import QtQuick.Timeline 1.0

Window {
    visible: true
    visibility : Window.Maximized
    color: "#000000"
    Item {
        id: container
        anchors.centerIn: parent
        width: parent.width - 16
        height: parent.height - 16
        Column {
            anchors.fill: parent
            spacing: 8
            Item {
                id: rpmMeter
                width: parent.width
                height: parent.height * 0.12
                Row {
                    anchors.fill: parent
                    Repeater {
                        model: 64
                         Rectangle {
                             width: parent.width / 64
                             height: parent.height
                             border.width: 1
                             color: (index <= 52
                                     ? 'green'
                                     : 'red')
                         }
                    }
                }
            }
            Item {
                id: infoContainer
                width: parent.width
                height: parent.height * 0.88 - parent.spacing
                Row {
                    anchors.fill: parent
                    spacing: 8
                    Item {
                        width: parent.width * 0.3
                        height: parent.height
                        Column {
                            anchors.fill: parent
                            spacing: 12
                            Rectangle {
                                height: parent.height *0.25
                                width: parent.width
                                color: 'red'
                                Column {
                                    anchors.fill: parent
                                    Item {
                                        height: parent.height * 0.34
                                        width: parent.width
                                        Text {

                                            id: waterTempTitle
                                            anchors.fill: parent
                                            text: qsTr("Water Temp")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                    Item {
                                        height: parent.height * 0.66 - parent.spacing
                                        width: parent.width
                                        Text {
                                            id: waterTemp
                                            anchors.fill: parent
                                            text: qsTr("110")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                }
                            }
                            Item {
                                height: parent.height *0.25
                                width: parent.width
                                Column {
                                    anchors.fill: parent
                                    Item {
                                        height: parent.height * 0.34
                                        width: parent.width
                                        Text {
                                            id: oilTempTitle
                                            anchors.fill: parent
                                            text: qsTr("Oil Temp")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                    Item {
                                        height: parent.height * 0.66 - parent.spacing
                                        width: parent.width
                                        Text {
                                            id: oilTemp
                                            text: qsTr("58")
                                            anchors.fill: parent
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                }
                            }
                            Item {
                                height: parent.height *0.25
                                width: parent.width
                                Column {
                                    anchors.fill: parent
                                    Item {
                                        height: parent.height * 0.34
                                        width: parent.width
                                        Text {
                                            id: oilPressTitle
                                            anchors.fill: parent
                                            text: qsTr("Oil Press")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                    Item {
                                        height: parent.height * 0.66 - parent.spacing
                                        width: parent.width
                                        Text {
                                            id: oilPress
                                            text: qsTr("3.21")
                                            anchors.fill: parent
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                }
                            }
                        }
                    }
                    Item {
                        width: parent.width * 0.4 - parent.spacing*2
                        height: parent.height
                        Column {
                            anchors.fill: parent
                            spacing: 8
                            Item {
                                height: parent.height * 0.16
                                width: parent.width
                                Text {
                                    id: rpm
                                    anchors.fill: parent
                                    text: qsTr("4278")
                                    color: 'white'
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    font.pixelSize: parent.height * 0.64
                                }
                            }
                            Item {
                                height: parent.height * 0.6 - parent.spacing * 2
                                width: parent.width
                                Text {
                                    id: gear
                                    anchors.fill: parent
                                    text: qsTr("2")
                                    color: 'yellow'
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    font.pixelSize: parent.height * 0.88
                                }
                            }
                            Item {
                                height: parent.height * 0.24
                                width: parent.width
                                Text {
                                    id: speed
                                    anchors.fill: parent
                                    text: qsTr("23")
                                    color: 'white'
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                    font.pixelSize: parent.height * 0.64
                                }
                            }
                        }
                    }
                    Item {
                        width: parent.width * 0.3
                        height: parent.height
                        Column {
                            anchors.fill: parent
                            spacing: 12
                            Rectangle {
                                height: parent.height *0.25
                                width: parent.width
                                color: 'black'
                                Column {
                                    anchors.fill: parent
                                    Item {
                                        height: parent.height * 0.34
                                        width: parent.width
                                        Text {

                                            id: waterTepTitle
                                            anchors.fill: parent
                                            text: qsTr("Fuel Remaining")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                    Item {
                                        height: parent.height * 0.66 - parent.spacing
                                        width: parent.width
                                        Text {
                                            id: wateTemp
                                            anchors.fill: parent
                                            text: qsTr("41")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                }
                            }
                            Item {
                                height: parent.height *0.25
                                width: parent.width
                                Column {
                                    anchors.fill: parent
                                    Item {
                                        height: parent.height * 0.34
                                        width: parent.width
                                        Text {
                                            id: oilTemTitle
                                            anchors.fill: parent
                                            text: qsTr("Time")
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                    Item {
                                        height: parent.height * 0.66 - parent.spacing
                                        width: parent.width
                                        Text {
                                            id: oiTemp
                                            text: qsTr("00:34")
                                            anchors.fill: parent
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                            font.pointSize: parent.height * 0.64
                                            color: 'white'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    }
}
