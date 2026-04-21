/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtWebChannel module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

"use strict";

var QWebChannelMessageTypes = {
    signal: 1,
    propertyUpdate: 2,
    init: 3,
    idle: 4,
    debug: 5,
    reply: 6,
    error: 7,
    invokeMethod: 8,
    connectToSignal: 9,
    disconnectFromSignal: 10,
    setProperty: 11,
    response: 12
};

var QWebChannel = function(transport, initCallback)
{
    if (typeof transport !== "object" || typeof transport.send !== "function") {
        console.error("The QWebChannel transport object is invalid!");
        return;
    }

    var channel = this;
    this.transport = transport;

    this.send = function(data)
    {
        if (typeof data !== "string") {
            data = JSON.stringify(data);
        }
        channel.transport.send(data);
    }

    this.transport.onmessage = function(message)
    {
        var data = message.data;
        if (typeof data === "string") {
            data = JSON.parse(data);
        }
        switch (data.type) {
            case QWebChannelMessageTypes.signal:
                channel.handleSignal(data);
                break;
            case QWebChannelMessageTypes.response:
                channel.handleResponse(data);
                break;
            case QWebChannelMessageTypes.propertyUpdate:
                channel.handlePropertyUpdate(data);
                break;
            default:
                console.error("invalid message type received: ", data.type);
                break;
        }
    }

    this.execCallbacks = {};
    this.execId = 0;
    this.exec = function(data, callback)
    {
        if (!callback) {
            channel.send(data);
            return;
        }
        var id = channel.execId++;
        channel.execCallbacks[id] = callback;
        data.id = id;
        channel.send(data);
    };

    this.objects = {};

    this.handleSignal = function(message)
    {
        var object = channel.objects[message.object];
        if (object) {
            object.signalEmitted(message.signal, message.args);
        } else {
            console.warn("Unhandled signal: " + message.object + "::" + message.signal);
        }
    }

    this.handleResponse = function(message)
    {
        if (!message.hasOwnProperty("id")) {
            console.error("Invalid response message received: ", JSON.stringify(message));
            return;
        }
        channel.execCallbacks[message.id](message.data);
        delete channel.execCallbacks[message.id];
    }

    this.handlePropertyUpdate = function(message)
    {
        for (var i in message.signals) {
            var signal = message.signals[i];
            var object = channel.objects[signal.object];
            if (object) {
                object.signalEmitted(signal.signal, signal.args);
            } else {
                console.warn("Unhandled signal: " + signal.object + "::" + signal.signal);
            }
        }

        for (var i in message.properties) {
            var property = message.properties[i];
            var object = channel.objects[property.object];
            if (object) {
                object.propertyUpdate(property.property, property.value);
            } else {
                console.warn("Unhandled property update: " + property.object + "::" + property.property);
            }
        }
    }

    this.debug = function(message)
    {
        channel.send({type: QWebChannelMessageTypes.debug, data: message});
    };

    this.exec({type: QWebChannelMessageTypes.init}, function(data) {
        for (var objectName in data) {
            var object = new QObject(objectName, data[objectName], channel);
        }

        // now look for property updates, and connect to signals
        for (var objectName in data) {
            var object = channel.objects[objectName];
            for (var i in object.__signals__) {
                var signalName = object.__signals__[i];
                object.connect(signalName);
            }
        }

        if (initCallback) {
            initCallback(channel);
        }
        channel.exec({type: QWebChannelMessageTypes.idle});
    });
};

function QObject(name, data, webChannel)
{
    this.__id__ = name;
    webChannel.objects[name] = this;
    this.__webChannel__ = webChannel;
    this.__signals__ = data.signals;
    this.__methods__ = data.methods;

    this.propertyUpdate = function(propertyName, propertyValue)
    {
        this[propertyName] = propertyValue;
        var signalName = propertyName + "Changed";
        if (this.__signals__.indexOf(signalName) !== -1) {
            this.signalEmitted(signalName, [propertyValue]);
        }
    }

    this.signalEmitted = function(signalName, args)
    {
        var callback = this[signalName];
        if (typeof callback === "function") {
            callback.apply(callback, args);
        }
    }

    this.connect = function(signalName)
    {
        this.__webChannel__.exec({
            type: QWebChannelMessageTypes.connectToSignal,
            object: this.__id__,
            signal: signalName
        });
    }

    this.disconnect = function(signalName)
    {
        this.__webChannel__.exec({
            type: QWebChannelMessageTypes.disconnectFromSignal,
            object: this.__id__,
            signal: signalName
        });
    }

    // set property
    this.setProperty = function(propertyName, propertyValue)
    {
        this.__webChannel__.exec({
            type: QWebChannelMessageTypes.setProperty,
            object: this.__id__,
            property: propertyName,
            value: propertyValue
        });
    }

    // create methods
    for (var i in data.methods) {
        var methodName = data.methods[i][0];
        this[methodName] = (function(methodName) {
            return function() {
                var args = [];
                var callback;
                for (var i = 0; i < arguments.length; ++i) {
                    if (typeof arguments[i] === "function")
                        callback = arguments[i];
                    else
                        args.push(arguments[i]);
                }

                webChannel.exec({
                    type: QWebChannelMessageTypes.invokeMethod,
                    object: this.__id__,
                    method: methodName,
                    args: args
                }, callback);
            };
        })(methodName);
    }

    // create properties
    for (var propertyName in data.properties) {
        this.propertyUpdate(propertyName, data.properties[propertyName]);
    }
}

if (typeof module !== 'undefined') {
    module.exports = {
        QWebChannel: QWebChannel
    };
}
