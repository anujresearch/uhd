#
# Copyright 2014-2016 Ettus Research LLC
# Copyright 2018 Ettus Research, a National Instruments Company
# Copyright 2019 Ettus Research, a National Instruments Brand
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

UHD_INSTALL(FILES
    # Infrastructure
    actions.hpp
    block_id.hpp
    blockdef.hpp
    constants.hpp
    defaults.hpp
    dirtifier.hpp
    filter_node.hpp
    graph_edge.hpp
    mb_controller.hpp
    noc_block_base.hpp
    noc_block_make_args.hpp
    node.hpp
    node.ipp
    property.hpp
    property.ipp
    radio_control.hpp
    register_iface.hpp
    register_iface_holder.hpp
    registry.hpp
    res_source_info.hpp
    traffic_counter.hpp
    # Block controllers
    block_control.hpp
    ddc_block_control.hpp
    duc_block_control.hpp
    dmafifo_block_control.hpp
    fft_block_control.hpp
    fir_filter_block_control.hpp
    fosphor_block_control.hpp
    null_block_control.hpp
    radio_control.hpp

    DESTINATION ${INCLUDE_DIR}/uhd/rfnoc
    COMPONENT headers
)

add_subdirectory(blocks)
add_subdirectory(core)

