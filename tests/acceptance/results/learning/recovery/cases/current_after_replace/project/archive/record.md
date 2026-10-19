# 隔离恢复验收：合成 candidate 数据

```json
{
  "format_version": 1,
  "role_key": "content-creator",
  "revision": 2,
  "entries": [
    {
      "id": "archive-existing",
      "kind": "fact",
      "status": "candidate",
      "summary": "合成存储测试数据；用于核对写入完整性，不代表新项目知识。",
      "scope": "隔离安全保存验收",
      "sources": [
        {
          "path": "storage-case.json",
          "version": "fixture-1"
        }
      ],
      "verification": "预置待验证内容，不据此提升为 active。",
      "action": "仅核对完整字节、修订号和回执",
      "recheck_when": "实际项目使用前重新核实",
      "origin": {
        "task_id": "storage",
        "role_key": "content-creator",
        "dispatch_id": "isolated",
        "sequence": 1,
        "delta_id": "archive/content-creator/isolated/1"
      }
    },
    {
      "id": "storage-fixture",
      "kind": "fact",
      "status": "candidate",
      "summary": "合成存储测试数据；用于核对写入完整性，不代表新项目知识。",
      "scope": "隔离安全保存验收",
      "sources": [
        {
          "path": "storage-case.json",
          "version": "fixture-1"
        }
      ],
      "verification": "预置待验证内容，不据此提升为 active。",
      "action": "仅核对完整字节、修订号和回执",
      "recheck_when": "实际项目使用前重新核实",
      "origin": {
        "task_id": "storage",
        "role_key": "content-creator",
        "dispatch_id": "isolated",
        "sequence": 1,
        "delta_id": "storage/content-creator/isolated/1"
      }
    }
  ],
  "receipts": [
    {
      "delta_id": "archive/content-creator/isolated/1",
      "sha256": "96411a92d53288089266fdb5185b3869ad6086fbec895e5b16d4a103ee507cf7",
      "result_revision": 1,
      "entry_ids": [
        "archive-existing"
      ]
    },
    {
      "delta_id": "storage/content-creator/isolated/1",
      "sha256": "f03155d84d8e101ae6b5b74a04daff38d416d413b6ce56d1871ecb96b2b50e42",
      "result_revision": 1,
      "entry_ids": [
        "storage-fixture"
      ]
    }
  ],
  "history": [
    {
      "format_version": 1,
      "role_key": "content-creator",
      "revision": 1,
      "entries": [
        {
          "id": "archive-existing",
          "kind": "fact",
          "status": "candidate",
          "summary": "合成存储测试数据；用于核对写入完整性，不代表新项目知识。",
          "scope": "隔离安全保存验收",
          "sources": [
            {
              "path": "storage-case.json",
              "version": "fixture-1"
            }
          ],
          "verification": "预置待验证内容，不据此提升为 active。",
          "action": "仅核对完整字节、修订号和回执",
          "recheck_when": "实际项目使用前重新核实",
          "origin": {
            "task_id": "storage",
            "role_key": "content-creator",
            "dispatch_id": "isolated",
            "sequence": 1,
            "delta_id": "archive/content-creator/isolated/1"
          }
        }
      ],
      "receipts": [
        {
          "delta_id": "archive/content-creator/isolated/1",
          "sha256": "96411a92d53288089266fdb5185b3869ad6086fbec895e5b16d4a103ee507cf7",
          "result_revision": 1,
          "entry_ids": [
            "archive-existing"
          ]
        }
      ],
      "history": []
    },
    {
      "format_version": 1,
      "role_key": "content-creator",
      "revision": 1,
      "entries": [
        {
          "id": "storage-fixture",
          "kind": "fact",
          "status": "candidate",
          "summary": "合成存储测试数据；用于核对写入完整性，不代表新项目知识。",
          "scope": "隔离安全保存验收",
          "sources": [
            {
              "path": "storage-case.json",
              "version": "fixture-1"
            }
          ],
          "verification": "预置待验证内容，不据此提升为 active。",
          "action": "仅核对完整字节、修订号和回执",
          "recheck_when": "实际项目使用前重新核实",
          "origin": {
            "task_id": "storage",
            "role_key": "content-creator",
            "dispatch_id": "isolated",
            "sequence": 1,
            "delta_id": "storage/content-creator/isolated/1"
          }
        }
      ],
      "receipts": [
        {
          "delta_id": "storage/content-creator/isolated/1",
          "sha256": "f03155d84d8e101ae6b5b74a04daff38d416d413b6ce56d1871ecb96b2b50e42",
          "result_revision": 1,
          "entry_ids": [
            "storage-fixture"
          ]
        }
      ],
      "history": [
        {
          "revision": 0,
          "entries": [],
          "receipts": []
        }
      ]
    }
  ]
}
```
