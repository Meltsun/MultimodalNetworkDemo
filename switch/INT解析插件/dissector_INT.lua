-- @brief In-band Network Telementry dissector plugin
-- @author xu ziheng
-- @date 2024.04.11

-- create a new dissector
local NAME = "INT"
local PORT = 2066
local INT = Proto(NAME, "In-band Netowrk Telementry Protocol")

-- create fields of INT
local fields = INT.fields

-- fwd长度
fields.hop_cnt = ProtoField.uint8 ("INT.hop_cnt", "Hop Count")

-- data长度
fields.data_cnt = ProtoField.uint8 ("INT.data_cnt", "Data Count")

-- fwd内容
fields.fwd = ProtoField.none("INT.fwd", "Hop Data")

-- data内容
fields.data = ProtoField.none("INT.data", "INT Data")
--[[
fields.data0 = ProtoField.none("INT.data0", "INT Data[0]")
fields.data1 = ProtoField.none("INT.data1", "INT Data[1]")
fields.data2 = ProtoField.none("INT.data2", "INT Data[2]")
fields.data3 = ProtoField.none("INT.data3", "INT Data[3]")
fields.data4 = ProtoField.none("INT.data4", "INT Data[4]")
fields.data5 = ProtoField.none("INT.data5", "INT Data[5]")
fields.data6 = ProtoField.none("INT.data6", "INT Data[6]")
fields.data7 = ProtoField.none("INT.data7", "INT Data[7]")
fields.data8 = ProtoField.none("INT.data8", "INT Data[8]")
fields.data9 = ProtoField.none("INT.data9", "INT Data[9]")
data_fields = {fields.data0, fields.data1, fields.data2, fields.data3, fields.data4, fields.data5, fields.data6, fields.data7, fields.data8, fields.data9}
]]

fields.swid = ProtoField.uint8 ("INT.swid", "Swid")
fields.port_ingress = ProtoField.uint8 ("INT.port_ingress", "Ingress Port")
fields.port_engress = ProtoField.uint8 ("INT.port_ingress", "Egress Port")
fields.byte_ingress = ProtoField.uint32 ("INT.byte_ingress", "Ingress Byte")
fields.byte_engress = ProtoField.uint32 ("INT.byte_ingress", "Egress Byte")
fields.count_ingress = ProtoField.uint32 ("INT.count_ingress", "Ingress Count")
fields.count_engress = ProtoField.uint32 ("INT.count_ingress", "Egress Count")
fields.last_time_ingress = ProtoField.uint32 ("INT.last_time_ingress", "Ingress Last Time")
fields.last_time_engress = ProtoField.uint32 ("INT.last_time_engress", "Egress Last Time")
fields.current_time_ingress = ProtoField.uint32 ("INT.current_time_ingress", "Ingress Current Time")
fields.current_time_engress = ProtoField.uint32 ("INT.current_time_engress", "Egress Current Time")
fields.qdepth = ProtoField.uint32 ("INT.qdepth", "Queue Depth")

-- dissect packet
function INT.dissector (tvb, pinfo, tree)
    local offset = 0
	local tvb_len = tvb:len()
	local subtree = tree:add(INT, tvb:range(offset, tvb_len))

    -- show protocol name in protocol column
	pinfo.cols.protocol:set("INT")
	pinfo.cols.info:set("In-band Netowrk Telementry Protocol")

    -- dissect field one by one, and add to protocol tree
    -- 显示fwd长度
    subtree:add(fields.hop_cnt, tvb:range(offset, 1))
    local hop_cnt_bytes = tvb:bytes(offset,1)
	offset = offset + 1
    -- 显示data长度
    subtree:add(fields.data_cnt, tvb:range(offset, 1))
    local data_cnt_bytes = tvb:bytes(offset,1)
	offset = offset + 1

    -- 显示fwd内容(字符串形式)
    local offset_fwd = offset
    local hop_cnt_hex = hop_cnt_bytes:tohex()
    local hop_cnt_number = tonumber(hop_cnt_hex, 16)
    local length_per_hop = 1
    local fwdsubtree = subtree:add(fields.fwd, tvb:range(offset_fwd, hop_cnt_number * length_per_hop))
    local fwd_number_1 = ''
    for i=hop_cnt_number, 1, -1 do
        local fwd_bytes = tvb:bytes(offset_fwd, length_per_hop)
        local fwd_hex = fwd_bytes:tohex()
        local fwd_number = tostring(tonumber(fwd_hex, 16))
        fwd_number_1 = fwd_number_1 .. '-' .. fwd_number
        offset_fwd = offset_fwd + 1
    end
    fwdsubtree:append_text(":  " .. fwd_number_1)
    offset = offset_fwd

    --[[
    -- 显示fwd内容(tree形式)
    local offset_fwd = offset
    local hop_cnt_hex = hop_cnt_bytes:tohex()
    local hop_cnt_number = tonumber(hop_cnt_hex, 16)
    local fwdsubtree = subtree:add(fields.fwd, tvb:range(offset_fwd, hop_cnt_number))
    for i=hop_cnt_number, 1, -1 do
        local fwd_bytes = tvb:bytes(offset_fwd, 1)
        local fwd_hex = fwd_bytes:tohex()
        local fwd_number = tonumber(fwd_hex, 16)
        local fwd = fwd_bytes:tvb("Switch ID")
        local fwdtree = fwdsubtree:add(fields.fwd, fwd:range())
        fwdtree:append_text(":  "..fwd_number)
        offset_fwd = offset_fwd + 1
    end
    offset = offset_fwd
    ]]

    -- 显示data内容(tree形式)
    local offset_data = offset
    local data_cnt_hex = data_cnt_bytes:tohex()
    local data_cnt_number = tonumber(data_cnt_hex, 16)
    local length_per_data = 47
    local datasubtree = subtree:add(fields.data, tvb:range(offset_data, data_cnt_number * length_per_data))
    for i=data_cnt_number, 1, -1 do
        local data_bytes = tvb:bytes(offset_data, length_per_data)
        local data_hex = data_bytes:tohex()
        local data_number = tonumber(data_hex, 16)
        local data = data_bytes:tvb("Data")
        local datatree = datasubtree:add(fields.data, data:range())
        --local datatree = datasubtree:add(data_fields[data_cnt_number-i], data:range())

        local swid_bytes = tvb:bytes(offset_data, 1)
        local swid_hex = swid_bytes:tohex()
        local swid_number = tonumber(swid_hex, 16)
        offset_data = offset_data + 1

        local port_ingress_bytes = tvb:bytes(offset_data, 1)
        local port_ingress_hex = port_ingress_bytes:tohex()
        local port_ingress_number = tonumber(port_ingress_hex, 16)
        offset_data = offset_data + 1

        local port_egress_bytes = tvb:bytes(offset_data, 1)
        local port_egress_hex = port_egress_bytes:tohex()
        local port_egress_number = tonumber(port_egress_hex, 16)
        offset_data = offset_data + 1

        local byte_ingress_bytes = tvb:bytes(offset_data, 4)
        local byte_ingress_hex = byte_ingress_bytes:tohex()
        local byte_ingress_number = tonumber(byte_ingress_hex, 16)
        offset_data = offset_data + 4

        local byte_egress_bytes = tvb:bytes(offset_data, 4)
        local byte_egress_hex = byte_egress_bytes:tohex()
        local byte_egress_number = tonumber(byte_egress_hex, 16)
        offset_data = offset_data + 4

        local count_ingress_bytes = tvb:bytes(offset_data, 4)
        local count_ingress_hex = count_ingress_bytes:tohex()
        local count_ingress_number = tonumber(count_ingress_hex, 16)
        offset_data = offset_data + 4

        local count_egress_bytes = tvb:bytes(offset_data, 4)
        local count_egress_hex = count_egress_bytes:tohex()
        local count_egress_number = tonumber(count_egress_hex, 16)
        offset_data = offset_data + 4

        local last_time_ingress_bytes = tvb:bytes(offset_data, 6)
        local last_time_ingress_hex = last_time_ingress_bytes:tohex()
        local last_time_ingress_number = tonumber(last_time_ingress_hex, 16)
        local last_time_ingress_t = os.date("%Y-%m-%d %H:%M:%S", last_time_ingress_number)
        offset_data = offset_data + 6

        local last_time_egress_bytes = tvb:bytes(offset_data, 6)
        local last_time_egress_hex = last_time_egress_bytes:tohex()
        local last_time_egress_number = tonumber(last_time_egress_hex, 16)
        local last_time_egress_t = os.date("%Y-%m-%d %H:%M:%S", last_time_egress_number)
        offset_data = offset_data + 6

        local current_time_ingress_bytes = tvb:bytes(offset_data, 6)
        local current_time_ingress_hex = current_time_ingress_bytes:tohex()
        local current_time_ingress_number = tonumber(current_time_ingress_hex, 16)
        local current_time_ingress_t = os.date("%Y-%m-%d %H:%M:%S", current_time_ingress_number)
        offset_data = offset_data + 6

        local current_time_egress_bytes = tvb:bytes(offset_data, 6)
        local current_time_egress_hex = current_time_egress_bytes:tohex()
        local current_time_egress_number = tonumber(current_time_egress_hex, 16)
        local current_time_egress_t = os.date("%Y-%m-%d %H:%M:%S", current_time_egress_number)
        offset_data = offset_data + 6

        local qdepth_bytes = tvb:bytes(offset_data, 4)
        local qdepth_hex = qdepth_bytes:tohex()
        local qdepth_number = tonumber(qdepth_hex, 16)
        offset_data = offset_data + 4

        datatree:append_text(":  " .. '___' .. swid_number .. '___' .. port_ingress_number .. '___' .. port_egress_number .. '___' .. byte_ingress_number .. '___' .. byte_egress_number .. '___' .. count_ingress_number .. '___' .. count_egress_number .. '___' .. last_time_ingress_number .. '___' .. last_time_egress_number .. '___' .. current_time_ingress_number .. '___' .. current_time_egress_number .. '___' .. qdepth_number)
    end
    offset = offset_data
    
end

-- register this dissector
DissectorTable.get("ethertype"):add(PORT, INT)