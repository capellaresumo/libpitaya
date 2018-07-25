{
    'variables': {
        'build_for_linux%': "false",
        'build_for_mac%': "false",
        'build_for_windows%': "false",
        'build_for_ios%': "false",
        'build_for_android%': "false",

        'pitaya_library%': "static_library",
        'use_sys_openssl%': "true",
        'library%': "static_library",
        'use_sys_uv%': "false",
        'use_sys_zlib%': "false",
        'no_tls_support%': "false",
        'no_uv_support%': "false",
        'build_pypitaya%': "false",
        'python_header%': "/usr/include/python2.7",
        'build_jpitaya%': "false",
        'build_type%': "Release",
        'use_xcode%': "false",

        'pitaya_target%': "pitaya",
    },

    'target_defaults': {
        'default_configuration': 'Release_x64',
        'configurations': {
            'Release_x64': {
                'msvs_configuration_platform': 'x64',
            },
            'conditions': [
                ['build_for_ios == "true"', {
                    'xcode_settings': {
                        'SDKROOT': 'iphoneos',
                        'IPHONEOS_DEPLOYMENT_TARGET': '8.2',
                        'TARGETED_DEVICE_FAMILY': '1,2',
                        'CODE_SIGN_IDENTITY': 'iPhone Developer',
                        'ARCHS': '$(ARCHS_STANDARD_32_64_BIT)',
                    }, 
                }],
            ],
        },
        'conditions': [
            ['build_for_windows == "true"', {
                'msvs_settings': {
                    'VCCLCompilerTool': {
                        # 'AdditionalOptions': [ '/TP' ],
                    },
                },
                'defines': [
                    '_WIN32',
                    'WIN32',
                    '_CRT_NONSTDC_NO_DEPRECATE',
                    '_WINDOWS',
                    '_WINDLL',
                    'UNICODE',
                    '_UNICODE',
                ],
                'link_settings': {
                    'libraries': [
                        '-ladvapi32.lib',
                        '-liphlpapi.lib',
                        '-lpsapi.lib',
                        '-lshell32.lib',
                        '-lws2_32.lib'
                    ],
                },
            }, {  # else
                'defines': [
                  '_LARGEFILE_SOURCE',
                    '_FILE_OFFSET_BITS=64',
                    '_GNU_SOURCE'
                ]
            }],   # OS == "win"
            ['use_xcode == "false"', {
                'product_dir': 'output',
            }],
            ['build_type=="Debug"', {
                'cflags': ['-g', '-O0', '-Wall', '-Wextra', '-pedantic', '-fsanitize=address', '-fno-omit-frame-pointer']
            }],
            ['build_type=="Release"', {
                'cflags': ['-g', '-O3', '-Wall', '-Wextra', '-pedantic']
            }],
            ['build_for_android == "true"', {
                'defines': ['__ANDROID__'],
            }],
            ['use_sys_zlib == "true"', {
                'link_settings': {
                    'libraries': ['-lz'],
                },
            }, {
                'dependencies': [
                    './deps/zlib/zlib.gyp:zlib',
                ],
            }],
            ['no_uv_support == "false"', {
                'conditions': [
                    ['use_sys_uv == "false"', {
                        'dependencies': [
                            './deps/libuv/uv.gyp:libuv',
                        ],
                        'include_dirs': [
                            './deps/libuv/include',
                        ]
                    }, {
                        'link_settings': {
                            'libraries': ['-luv']
                        }
                    }],  # use_sys_uv
                    ['no_tls_support == "false"', {
                        'conditions': [
                            ['use_sys_openssl == "false"', {
                                'libraries': [
                                    '<!(pwd)/build/openssl/lib/libssl.a',
                                    '<!(pwd)/build/openssl/lib/libcrypto.a'
                                ],
                                'include_dirs': [
                                    '<!(pwd)/build/openssl/include',
                                ]
                            }, {
                                'conditions': [
                                    ['build_for_windows=="true"', {
                                        'libraries': [
                                            'C:/OpenSSL-Win64/lib/libeay32.lib',
                                            'C:/OpenSSL-Win64/lib/ssleay32.lib',
                                        ],
                                        'include_dirs': [
                                            'C:/OpenSSL-Win64/include',
                                        ],
                                    }, {
                                        'include_dirs': [
                                            './deps/openssl/openssl/include',
                                        ],
                                        'link_settings': {
                                            'libraries': [
                                                '-lssl',
                                                '-lcrypto',
                                            ],
                                        },
                                    }],
                                ],
                            }],  # use_sys_openssl
                        ],
                    }],  # no tls support
                ]
            }],  # no uv support
        ],
    },

    'targets': [
        {
            'target_name': '<(pitaya_target)',
            'include_dirs': [
                './include',
                './src',
            ],
            'sources': [
                './src/pc_pitaya.c',
                './src/pc_lib.c',
                './src/pc_unity.c',
                './src/pc_trans.c',
                './src/pc_assert.c',
                './src/pc_trans_repo.c',
                './src/pc_JSON.c',
                './src/tr/dummy/tr_dummy.c'
            ],
            'conditions': [
                ['no_tls_support=="true"', {
                    'defines': ['PC_NO_UV_TLS_TRANS']
                }],
                ['build_for_windows == "false"', {
                    'cflags': ['-fPIC'],
                }],
                ['build_for_mac == "true"', {
                    'product_extension': 'bundle',
                }],
                ['build_for_windows == "false"', {
                    'defines': ['_GNU_SOURCE'],
                    'cflags': ['-fPIC'],
                }, {
                    'defines': [
                        '_CRT_SECURE_NO_WARNINGS',
                        '_CRT_NONSTDC_NO_DEPRECATE',
                    ]
                }],
                ['build_for_android == "true"', {
                    'cflags': [
                        '-fPIE',
                        '-march=armv7-a',
                        '-mthumb',
                        '-fPIC',
                    ],
                    'link_settings': {
                        'libraries': ['-pie', '-llog'],
                    },
                }],
                ['build_for_ios == "true"', {
                    'type': 'static_library',
                }, {
                    'type': 'shared_library',
                    'defines': ['BUILDING_PC_SHARED=1'],
                }],
                ['no_uv_support == "false"', {
                    'sources': [
                        './src/tr/uv/pr_gzip.c',
                        './src/tr/uv/pr_msg.c',
                        './src/tr/uv/pr_msg_json.c',
                        './src/tr/uv/pr_pkg.c',
                        './src/tr/uv/tr_uv_tcp.c',
                        './src/tr/uv/tr_uv_tcp_i.c',
                        './src/tr/uv/tr_uv_tcp_aux.c',
                    ],
                    'conditions': [
                        ['no_tls_support == "false"', {
                            'sources': [
                                './src/tr/uv/tr_uv_tls.c',
                                './src/tr/uv/tr_uv_tls_i.c',
                                './src/tr/uv/tr_uv_tls_aux.c',
                            ]
                        }, {
                            'defines': ['PC_NO_UV_TLS_TRANS']
                        }],
                    ]}, {
                    'defines': ['PC_NO_UV_TCP_TRANS']
                }
                ],  # no uv support
            ],
        },
    ],
    'conditions': [
        ['build_for_mac == "true" or build_for_linux == "true" or build_for_windows == "true"', {
            'targets': [
                {
                    'target_name': 'tests',
                    'type': 'executable',
                    'dependencies': [
                        '<(pitaya_target)',
                    ],
                    'include_dirs': [
                        './include/',
                        '/usr/local/include',
                        './deps/munit',
                        './deps/nanopb-0.3.9.1',
                    ],
                    'sources': [
                        './test/main.c',
                        './test/test-tr_tcp.c',
                        './test/test-tr_tls.c',
                        './test/test_pc_client.c',
                        './test/test_reconnection.c',
                        './test/test_compression.c',
                        './test/test_kick.c',
                        './test/test_push.c',
                        './test/test_session.c',
                        './test/test_request.c',
                        './test/test_notify.c',
                        './test/test_stress.c',
                        './test/test_protobuf.c',
                        './deps/munit/munit.c',
                        './deps/nanopb-0.3.9.1/pb_decode.c',
                        './deps/nanopb-0.3.9.1/pb_encode.c',
                        './deps/nanopb-0.3.9.1/pb_common.c',
                        # proto files
                        './test/error.pb.c',
                        './test/session-data.pb.c',
                        './test/response.pb.c',
                        './test/big-message.pb.c',
                    ],
                },
            ],
        }],
        ['build_pypitaya == "true"', {
            'targets': [{
                'target_name': 'pypitaya',
                'type': 'shared_library',
                'dependencies': [
                    '<(pitaya_target)',
                ],
                'include_dirs': [
                    './include/',
                    '<(python_header)',
                ],
                'sources': [
                    './py/pypitaya.c',
                ],
            }],
        }],
        ['build_jpitaya == "true"', {
            'targets': [{
                'target_name': 'jpitaya',
                'type': 'shared_library',
                'dependencies': [
                    '<(pitaya_target)',
                ],
                'include_dirs': [
                    './include/',
                ],
                'sources': [
                    './java/com_netease_pomelo_Client.c',
                ],
            }],
        }],
    ],
}
